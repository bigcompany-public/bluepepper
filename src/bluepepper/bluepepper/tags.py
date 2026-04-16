from __future__ import annotations

import logging
from typing import Optional

from pymongo.collection import Collection

from bluepepper.core import codex, database


class TagAlreadyExistsError(Exception):
    """Raised when attempting to create a tag that already exists in the database."""

    ...


class TagCreator:
    def __init__(
        self,
        tag: str,
        color: Optional[str] = "#45AB9E",
        text_color: Optional[str] = "#FFFFFF",
        icon: Optional[str] = "fa5s.circle",
        icon_color: Optional[str] = "#FFFFFF",
    ) -> None:
        self.tag = tag
        self.icon = icon
        self.color = color
        self.text_color = text_color
        self.icon_color = icon_color
        self.document: Optional[dict] = None

    @property
    def fields(self) -> dict:
        return {
            "tag": self.tag,
            "tagColor": self.color,
            "tagTextColor": self.text_color,
            "tagIcon": self.icon,
            "tagIconColor": self.icon_color,
        }

    def create(self) -> dict:
        try:
            self.check_field_rules()
            self.create_db_document()
        except Exception:
            logging.error("An error occured while creating the asset tag")
            raise
        return self.document  # type: ignore

    def check_field_rules(self):
        codex.rules.tag.match(self.tag, raise_exception=True)

    def create_db_document(self) -> dict:
        """Creates the document on the database"""
        self.check_existing_tag()
        result = self.collection.insert_one(self.fields)
        if not result.inserted_id:
            raise RuntimeError(f"Failed to create tag on database : {self.fields}")
        result = self.collection.find_one(result.inserted_id)
        self.document = database.stringify_id(result)
        logging.info(
            f"Successfully created tag document on the database : {self.document}"
        )
        return self.document

    def check_existing_tag(self) -> None:
        query = {"tag": self.tag}
        result = list(self.collection.find(query))
        if result:
            raise TagAlreadyExistsError(f"Tag already exists : {query}")

    @property
    def collection(self) -> Collection:
        raise NotImplementedError("This property should be set in a derived class")


class AssetTagCreator(TagCreator):
    def __init__(
        self,
        tag: str,
        color: str | None = "#45AB9E",
        text_color: str | None = "#FFFFFF",
        icon: str | None = None,
        icon_color: str | None = "#FFFFFF",
    ) -> None:
        super().__init__(tag, color, text_color, icon, icon_color)

    @property
    def collection(self) -> Collection:
        return database.asset_tags


class ShotTagCreator(TagCreator):
    def __init__(
        self,
        tag: str,
        color: str | None = "#45AB9E",
        text_color: str | None = "#FFFFFF",
        icon: str | None = None,
        icon_color: str | None = "#FFFFFF",
    ) -> None:
        super().__init__(tag, color, text_color, icon, icon_color)

    @property
    def collection(self) -> Collection:
        return database.shot_tags
