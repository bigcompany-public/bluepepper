from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from functools import cached_property

from aquarium.aquarium import Asset as AqAsset
from aquarium.aquarium import Element
from aquarium.aquarium import Shot as AqShot
from bson import ObjectId

from bluepepper.aqua import get_aqua
from bluepepper.core import codex, database
from bluepepper.helpers.timeit import timeit


class AssetNotFoundError(Exception): ...


class Asset:
    def __init__(self, document_id: str):
        self.document_id = document_id

    @cached_property
    def document(self) -> dict:
        return database.get_asset_document_by_id(self.document_id)

    @cached_property
    def aquarium_asset(self) -> AqAsset:
        aqua = get_aqua()
        return aqua.get_asset_from_key(self.document["_aquariumKey"])

    @cached_property
    def identifier(self) -> str:
        return codex.convs.asset_identifier.format(self.document)

    @property
    def tags(self) -> list[str]:
        return self.document.get("_tags") or []

    def get_reverse_breakdown(self) -> list[Shot]:
        query = {f"_breakdown.{self.document['asset']}": {"$exists": True}}
        shot_documents = list(database.shots.find(query))
        shots = [Shot.from_document_id(doc["_id"]) for doc in shot_documents]
        return shots

    def add_tag(self, tag: str):
        # Raise error if asset tag was not found
        logging.info(f'Adding tag "{tag}" to asset : {self.identifier}')
        database.get_asset_tag_document_by_name(tag)
        all_tags: list = self.document.get("_tags", [])
        all_tags.append(tag)
        all_tags = sorted(list(set(all_tags)))
        database.assets.update_one(
            {"_id": ObjectId(self.document["_id"])}, {"$set": {"_tags": all_tags}}
        )

        # invalidate current document
        del self.document

    def remove_tag(self, tag: str):
        # Raise error if asset tag was not found
        database.get_asset_tag_document_by_name(tag)
        all_tags: list = self.document.get("_tags", [])
        if tag not in all_tags:
            return

        logging.info(f'Removing tag "{tag}" from asset : {self.identifier}')
        all_tags.remove(tag)
        database.assets.update_one(
            {"_id": ObjectId(self.document["_id"])}, {"$set": {"_tags": all_tags}}
        )

        # invalidate current document
        del self.document

    def __repr__(self) -> str:
        return f"Asset {self.identifier}:\n{json.dumps(self.document, indent=4)}"

    def __str__(self) -> str:
        return self.identifier

    @staticmethod
    def from_document_id(document_id: str) -> Asset:
        return Asset(document_id=document_id)

    @staticmethod
    def from_aquarium_key(aquarium_key: int) -> Asset:
        document: dict[str, str] = database.assets.find_one(
            {"_aquariumKey": int(aquarium_key)}
        )  # type: ignore
        if not document:
            raise AssetNotFoundError(
                f'Asset with aquarium key "{aquarium_key}" not found'
            )
        return Asset(document_id=document["_id"])

    @staticmethod
    def from_fields(fields: dict[str, str]) -> Asset:
        query = {
            k: v
            for k, v in fields.items()
            if k in codex.convs.asset_identifier.required_fields
        }
        document: dict[str, str] = database.assets.find_one(query)  # type: ignore
        if not document:
            raise AssetNotFoundError(f"Asset with query {query} not found")
        return Asset(document_id=document["_id"])


class ShotNotFoundError(Exception): ...


class Shot:
    def __init__(self, document_id: str):
        self.document_id = document_id

    @cached_property
    def document(self) -> dict:
        return database.get_shot_document_by_id(self.document_id)

    @cached_property
    def aquarium_shot(self) -> AqShot:
        aqua = get_aqua()
        return aqua.get_shot_from_key(self.document["_aquariumKey"])

    @cached_property
    def identifier(self) -> str:
        return codex.convs.shot_identifier.format(self.document)

    @property
    def tags(self) -> list[str]:
        return self.document.get("_tags") or []

    @timeit
    def _get_aqua_breakdown(self) -> dict[str, int]:
        logging.info(f"{self.identifier} - Fetching aquarium breakdown")
        meshql = "# -($Breakdown, 1)> $Asset UNIQUE"
        elements: list[Element] = self.aquarium_shot.traverse(meshql)
        breakdown = []
        for element in elements:
            asset: str = element["item"]["data"]["asset"]
            quantity: int = element["edge"]["data"].get("quantity", 1)
            breakdown.append((asset, quantity))
        breakdown.sort(key=lambda x: x[0])  # Sort by asset name
        return {asset: quantity for asset, quantity in breakdown}

    def update_database_breakdown(self) -> dict[str, int]:
        breakdown = self._get_aqua_breakdown()
        logging.info(f"{self.identifier} - Updating database breakdown")
        result = database.shots.update_one(
            filter={"_id": ObjectId(self.document["_id"])},
            update={"$set": {"_breakdown": breakdown}},
        )
        if not result.matched_count:
            raise RuntimeError(
                f"{self.identifier} - Failed to update the breakdown on database"
            )

        # invalidate current document
        del self.document

        return breakdown

    def get_breakdown(self) -> list[AssetCasting]:
        assets: list[AssetCasting] = []
        breakdown = self.document.get("_breakdown") or {}
        for asset_name, quantity in breakdown.items():
            asset = Asset.from_fields({"asset": asset_name})
            assets.append(AssetCasting(asset=asset, quantity=quantity))
        return assets

    def __repr__(self) -> str:
        return f"Shot {self.identifier}:\n{json.dumps(self.document, indent=4)}"

    def __str__(self) -> str:
        return self.identifier

    @staticmethod
    def from_document_id(document_id: str) -> Shot:
        return Shot(document_id=document_id)

    @staticmethod
    def from_aquarium_key(aquarium_key: int) -> Shot:
        document: dict[str, str] = database.assets.find_one(
            {"_aquariumKey": int(aquarium_key)}
        )  # type: ignore
        if not document:
            raise ShotNotFoundError(
                f'Shot with aquarium key "{aquarium_key}" not found'
            )
        return Shot(document_id=document["_id"])

    @staticmethod
    def from_fields(fields: dict[str, str]) -> Shot:
        query = {
            k: v
            for k, v in fields.items()
            if k in codex.convs.asset_identifier.required_fields
        }
        document: dict[str, str] = database.assets.find_one(query)  # type: ignore
        if not document:
            raise ShotNotFoundError(f"Shot with query {query} not found")
        return Shot(document_id=document["_id"])

    def add_tag(self, tag: str):
        # Raise error if shot tag was not found
        logging.info(f'Adding tag "{tag}" to shot : {self.identifier}')
        database.get_shot_tag_document_by_name(tag)
        all_tags: list = self.document.get("_tags", [])
        all_tags.append(tag)
        all_tags = sorted(list(set(all_tags)))
        database.shots.update_one(
            {"_id": ObjectId(self.document["_id"])}, {"$set": {"_tags": all_tags}}
        )

        # invalidate current document
        del self.document

    def remove_tag(self, tag: str):
        # Raise error if shot tag was not found
        database.get_shot_tag_document_by_name(tag)
        all_tags: list = self.document.get("_tags", [])
        if tag not in all_tags:
            return

        logging.info(f'Removing tag "{tag}" from shot : {self.identifier}')
        all_tags.remove(tag)
        database.shots.update_one(
            {"_id": ObjectId(self.document["_id"])}, {"$set": {"_tags": all_tags}}
        )

        # invalidate current document
        del self.document


@dataclass
class AssetCasting:
    asset: Asset = field(repr=False)
    quantity: int = field(repr=False)

    def __str__(self):
        return f"{self.asset.identifier} x {self.quantity}"

    def __repr__(self):
        return f"{self.asset.identifier} x {self.quantity}"
