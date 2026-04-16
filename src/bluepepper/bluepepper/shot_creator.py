import logging
from argparse import ArgumentParser
from typing import Dict, Optional

from aquarium.aquarium import Shot as AqShot
from bson import ObjectId

from bluepepper.aqua import get_aqua
from bluepepper.core import codex, database, init_logging


class ShotAlreadyExistsError(Exception):
    """Raised when attempting to create an shot that already exists in the database."""

    ...


class ShotCreator:
    def __init__(self, fields: Dict[str, str]):
        self.fields = fields
        self.document: dict[str, str] = {}
        self.aquarium_shot: Optional[AqShot] = None

    def create(self):
        try:
            self.check_required_fields()
            self.check_field_rules()
            self.create_db_document()
            self.create_aquarium_shot()
        except Exception:
            logging.error("An error occured while creating the shot")
            self.remove_db_document()
            self.remove_aquarium_shot()
            raise

    def check_required_fields(self):
        """Check if all the fields needed to properly identify the entity are passed by the user."""
        missing_fields: list[str] = []
        for field in codex.convs.shot_fields.required_fields:
            if field not in self.fields:
                missing_fields.append(field)

        if missing_fields:
            message = [f"\t - {field}" for field in missing_fields]
            message = "\n".join(message)
            raise Exception(f"The following fields are required :\n{message}")

    def check_field_rules(self):
        """Raises an error if fields do not respect the rules"""
        codex.convs.shot_fields.format(self.fields)

    def create_db_document(self) -> dict[str, str]:
        """Creates the shot document on the database"""
        self.check_existing_shot()
        result = database.shots.insert_one(self.fields)
        if not result.inserted_id:
            raise RuntimeError(f"Failed to create shot on database : {self.fields}")
        self.document = database.get_shot_document_by_id(str(result.inserted_id))
        logging.info(
            f"Successfully created shot document on the database : {self.document}"
        )
        return self.document

    def check_existing_shot(self) -> None:
        query = {
            key: value
            for key, value in self.fields.items()
            if key in codex.convs.shot_identifier.required_fields
        }
        result = list(database.shots.find(query))
        if result:
            raise ShotAlreadyExistsError(
                f"An shot with these fields already exists : {query}"
            )

    def remove_db_document(self):
        if not self.document:
            return
        logging.warning(f"Removing document from the database {self.document}")
        database.shots.delete_one({"_id": ObjectId(self.document["_id"])})

    def create_aquarium_shot(self):
        """Creates the shot on aquarium, and fills the "_aquariumKey" field on the database"""
        aqua = get_aqua()
        aq_shot = aqua.create_shot(self.document)
        self.aquarium_shot = aq_shot
        database.shots.update_one(
            {"_id": ObjectId(self.document["_id"])},
            {"$set": {"_aquariumKey": int(aq_shot._key)}},
        )

    def remove_aquarium_shot(self) -> None:
        if not self.aquarium_shot:
            return
        logging.warning("Removing aquarium shot")
        self.aquarium_shot.trash()


if __name__ == "__main__":
    init_logging("shotCreator")
    parser = ArgumentParser()
    parser.add_argument("-se", "--season", required=True, type=str)
    parser.add_argument("-ep", "--episode", required=True, type=str)
    parser.add_argument("-sq", "--sequence", required=True, type=str)
    parser.add_argument("-sh", "--shot", required=True, type=str)
    args = parser.parse_args()

    fields = {
        "season": args.season,
        "episode": args.episode,
        "sequence": args.sequence,
        "shot": args.shot,
    }
    ac = ShotCreator(fields)
    ac.create()
