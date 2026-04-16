import logging
from argparse import ArgumentParser
from typing import Dict, Optional

from aquarium.aquarium import Asset as AqAsset
from bson import ObjectId
from conf.project import ProjectSettings

from bluepepper.aqua import get_aqua
from bluepepper.core import codex, database, init_logging


class AssetAlreadyExistsError(Exception):
    """Raised when attempting to create an asset that already exists in the database."""

    ...


class AssetCreator:
    def __init__(self, fields: Dict[str, str]):
        self.fields = fields.copy()
        self.document: dict[str, str] = {}
        self.aquarium_asset: Optional[AqAsset] = None

    def create(self):
        try:
            self.check_required_fields()
            self.check_field_rules()
            self.create_db_document()
            if "aquarium" in ProjectSettings.production_trackers:
                self.create_aquarium_asset()
        except Exception:
            logging.error("An error occured while creating the asset")
            self.remove_db_document()
            if "aquarium" in ProjectSettings.production_trackers:
                self.remove_aquarium_asset()
            raise

    def check_required_fields(self):
        """Check if all the fields needed to properly identify the entity are passed by the user."""
        missing_fields: list[str] = []
        for field in codex.convs.asset_fields.required_fields:
            if field not in self.fields:
                missing_fields.append(field)

        if missing_fields:
            message = [f"\t - {field}" for field in missing_fields]
            message = "\n".join(message)
            raise Exception(f"The following fields are required :\n{message}")

    def check_field_rules(self):
        """Raises an error if fields do not respect the rules"""
        codex.convs.asset_fields.format(self.fields)

    def create_db_document(self) -> dict[str, str]:
        """Creates the document on the database"""
        self.check_existing_asset()
        result = database.assets.insert_one(self.fields)
        if not result.inserted_id:
            raise RuntimeError(f"Failed to create asset on database : {self.fields}")
        self.document = database.get_asset_document_by_id(str(result.inserted_id))
        logging.info(f"Successfully created asset document on the database : {self.document}")
        return self.document

    def check_existing_asset(self) -> None:
        query = {
            key: value for key, value in self.fields.items() if key in codex.convs.asset_identifier.required_fields
        }
        result = list(database.assets.find(query))
        if result:
            raise AssetAlreadyExistsError(f"An asset with these fields already exists : {query}")

    def remove_db_document(self):
        if not self.document:
            return
        logging.warning(f"Removing document from the database {self.document}")
        database.assets.delete_one({"_id": ObjectId(self.document["_id"])})

    def create_aquarium_asset(self):
        """Creates the asset on aquarium, and fills the "_aquariumKey" field on the database"""
        if "aquarium" not in ProjectSettings.production_trackers:
            return
        aqua = get_aqua()
        aq_asset = aqua.create_asset(self.document)
        self.aquarium_asset = aq_asset
        database.assets.update_one(
            {"_id": ObjectId(self.document["_id"])},
            {"$set": {"_aquariumKey": int(aq_asset._key)}},
        )

    def remove_aquarium_asset(self):
        if "aquarium" not in ProjectSettings.production_trackers:
            return

        if not self.aquarium_asset:
            return
        logging.warning("Removing aquarium asset")
        self.aquarium_asset.trash()


if __name__ == "__main__":
    init_logging("assetCreator")
    parser = ArgumentParser()
    parser.add_argument("-a", "--asset", required=True, type=str)
    parser.add_argument("-t", "--type", required=True, type=str)
    args = parser.parse_args()

    fields = {
        "asset": args.asset,
        "type": args.type,
    }
    ac = AssetCreator(fields)
    ac.create()
