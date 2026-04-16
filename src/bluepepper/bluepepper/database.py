import logging
import os
import socket
import subprocess
from atexit import register
from functools import cached_property
from pathlib import Path
from typing import Any

from bson.objectid import ObjectId
from conf.database import DatabaseSettings
from conf.lucent_config import codex
from pymongo import MongoClient, errors
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database

# TODO : ajouter des retries avec le package "tenacity"


class AssetNotFoundError(Exception):
    """Raised when an asset document is not found in the database."""

    ...


class AssetTagNotFoundError(Exception):
    """Raised when an asset tag document is not found in the database."""

    ...


class ShotTagNotFoundError(Exception):
    """Raised when an asset tag document is not found in the database."""

    ...


class ShotNotFoundError(Exception):
    """Raised when a shot document is not found in the database."""

    ...


class BigMongoClient(MongoClient):
    """MongoDB client for the BluePepper animation pipeline.

    Handles connection management, local server startup, and document retrieval
    for assets and shots with robust error handling and retries.
    """

    def __init__(self) -> None:
        """Initialize connection to MongoDB with retries and fallback to local server.

        Attempts to connect to the configured MongoDB server. If connection fails
        and the server is configured as local, automatically starts a local
        MongoDB instance.

        Raises:
            errors.ConnectionFailure: If unable to connect to MongoDB server
                after retries and local startup attempts.
        """
        logging.info("Connecting to MongoDB database")
        logging.getLogger("pymongo").setLevel(logging.INFO)
        self.settings: DatabaseSettings = DatabaseSettings()
        super().__init__(
            self.settings.host,
            self.settings.port,
            username=self.settings.user,
            password=self.settings.password,
        )

        # Test connection on socket with fine-tuned timeout
        if not self.test_connection_retries(timeout_s=0.3, retries=3):
            if not self.is_local_server:
                msg = f"Failed to connect to MongoDB server {self.settings.host}:{self.settings.port}"
                raise errors.ConnectionFailure(msg)
            self.start_local_mongodb_server()

    def test_connection_retries(self, timeout_s: float, retries: int) -> bool:
        """Test MongoDB connection with multiple retries.

        Attempts to connect to the MongoDB server multiple times with the
        specified timeout per attempt.

        Args:
            timeout_s: Socket timeout in seconds for each connection attempt.
            retries: Number of connection attempts to make.

        Returns:
            True if connection successful on any attempt, False if all
            attempts fail.
        """
        for i in range(1, retries + 1):
            logging.debug(f"Testing MongoDB connection (attempt {i})")
            if self.test_connection(timeout_s):
                return True
        return False

    def test_connection(self, timeout_s: float) -> bool:
        """Test connection to MongoDB server using socket-level operations.

        Prevents features using MongoDB from freezing if server is unreachable.
        PyMongo's timeout is unreliable with very small timeouts, so we use
        socket-level testing instead.

        Args:
            timeout_s: Socket timeout in seconds for the connection attempt.

        Returns:
            True if socket connection to MongoDB server succeeds, False otherwise.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout_s)
        try:
            sock.connect((self.settings.host, self.settings.port))
            sock.shutdown(2)
            return True
        except (OSError, socket.timeout):
            return False
        finally:
            sock.close()

    @cached_property
    def db(self) -> Database:
        """Get the main database instance.

        Returns:
            MongoDB Database instance for the configured database name.
        """
        return self.get_database(self.settings.database_name)

    @cached_property
    def assets(self) -> Collection:
        """Get the assets collection.

        Returns:
            MongoDB Collection instance for assets.
        """
        return self.db.get_collection("assets")

    @cached_property
    def asset_tags(self) -> Collection:
        """Get the asset tags collection.

        Returns:
            MongoDB Collection instance for asset tags.
        """
        return self.db.get_collection("assetTags")

    @cached_property
    def shot_tags(self) -> Collection:
        """Get the shotTags collection.

        Returns:
            MongoDB Collection instance for shot tags.
        """
        return self.db.get_collection("shotTags")

    @cached_property
    def shots(self) -> Collection:
        """Get the shots collection.

        Returns:
            MongoDB Collection instance for shots.
        """
        return self.db.get_collection("shots")

    @cached_property
    def episodes(self) -> Collection:
        """Get the episodes collection.

        Returns:
            MongoDB Collection instance for episodes.
        """
        return self.db.get_collection("episodes")

    def ensure_structure(self) -> None:
        """Ensure database has required collections with sample documents.

        Creates sample documents in each collection if they are empty.
        Used for initial database setup and verification.
        """
        if not self.assets.find_one():
            self.assets.insert_one({"asset": "pear", "type": "prp", "group": "dev"})

        if not self.shots.find_one():
            self.shots.insert_one({"shot": "sh9999", "sequence": "sq9999", "episode": "ep999"})

        if not self.episodes.find_one():
            self.episodes.insert_one({"episode": "ep999"})

    @property
    def is_local_server(self) -> bool:
        """Check if MongoDB server is configured as local.

        Returns:
            True if configured host is localhost or 127.0.0.1, False otherwise.
        """
        return self.settings.host in ("127.0.0.1", "localhost")

    def get_asset_document_by_id(self, document_id: str) -> dict[str, Any]:
        """Retrieve asset document by ObjectId.

        Args:
            document_id: Asset document ID as string representation of ObjectId.

        Returns:
            Asset document dictionary with _id converted to string.

        Raises:
            AssetNotFoundError: If no asset with the given ID exists.
        """
        document = self.assets.find_one(ObjectId(document_id))
        if not document:
            raise AssetNotFoundError(f'No asset with _id="{document_id}" was found')
        return self.stringify_id(document)

    def get_asset_document_by_name(self, asset_name: str) -> dict[str, Any]:
        """Retrieve asset document by asset name.

        Args:
            asset_name: The asset name to search for.

        Returns:
            Asset document dictionary with _id converted to string.

        Raises:
            AssetNotFoundError: If no asset with the given name exists.
        """
        document = self.assets.find_one({"asset": asset_name})
        if not document:
            raise AssetNotFoundError(f'No asset with asset="{asset_name}" was found')
        return self.stringify_id(document)

    def get_asset_document_by_fields(self, fields: dict[str, Any]) -> dict[str, Any]:
        """Retrieve asset document by multiple required fields.

        Validates that all required fields for asset identification are present
        in the provided dictionary before querying the database.

        Args:
            fields: Dictionary of field names and values to query. Must contain
                all required fields defined in codex.convs.asset_identifier.

        Returns:
            Asset document dictionary with _id converted to string.

        Raises:
            KeyError: If any required fields for asset identification are
                missing or empty in the provided fields dictionary.
            AssetNotFoundError: If no asset matches the query criteria.
        """
        missing = []
        query: dict[str, Any] = {}
        for field in codex.convs.asset_identifier.required_fields:
            value = fields.get(field)
            if not value:
                missing.append(field)
            else:
                query[field] = value

        if missing:
            raise KeyError(f"Missing required fields for asset query: {missing}")

        document = self.assets.find_one(query)
        if not document:
            raise AssetNotFoundError(f"No asset found with query: {query}")
        return self.stringify_id(document)

    def get_asset_document_by_string(self, string: str) -> dict[str, Any]:
        """Retrieve asset document from parsed string identifier.

        Parses the string using codex to extract fields, then queries the
        database for a matching asset.

        Args:
            string: Asset identifier string to parse and use for querying.

        Returns:
            Asset document dictionary with _id converted to string.

        Raises:
            AssetNotFoundError: If no asset matches the parsed string fields.
        """
        fields = codex.get_fields(string)
        return self.get_asset_document_by_fields(fields)

    def get_shot_document_by_id(self, document_id: str) -> dict[str, Any]:
        """Retrieve shot document by ObjectId.

        Args:
            document_id: Shot document ID as string representation of ObjectId.

        Returns:
            Shot document dictionary with _id converted to string.

        Raises:
            ShotNotFoundError: If no shot with the given ID exists.
        """
        document = self.shots.find_one(ObjectId(document_id))
        if not document:
            raise ShotNotFoundError(f'No shot with _id="{document_id}" was found')
        return self.stringify_id(document)

    def get_shot_document_by_name(self, shot_name: str) -> dict[str, Any]:
        """Retrieve shot document by shot name.

        Args:
            shot_name: The shot name to search for.

        Returns:
            Shot document dictionary with _id converted to string.

        Raises:
            ShotNotFoundError: If no shot with the given name exists.
        """
        document = self.shots.find_one({"shot": shot_name})
        if not document:
            raise ShotNotFoundError(f'No shot with shot="{shot_name}" was found')
        return self.stringify_id(document)

    def get_shot_document_by_fields(self, fields: dict[str, Any]) -> dict[str, Any]:
        """Retrieve shot document by multiple required fields.

        Validates that all required fields for shot identification are present
        in the provided dictionary before querying the database.

        Args:
            fields: Dictionary of field names and values to query. Must contain
                all required fields defined in codex.convs.shot_identifier.

        Returns:
            Shot document dictionary with _id converted to string.

        Raises:
            KeyError: If any required fields for shot identification are
                missing or empty in the provided fields dictionary.
            ShotNotFoundError: If no shot matches the query criteria.
        """
        missing = []
        query: dict[str, Any] = {}
        for field in codex.convs.shot_identifier.required_fields:
            value = fields.get(field)
            if not value:
                missing.append(field)
            else:
                query[field] = value

        if missing:
            raise KeyError(f"Missing required fields for shot query: {missing}")

        document = self.shots.find_one(query)
        if not document:
            raise ShotNotFoundError(f"No shot found with query: {query}")
        return self.stringify_id(document)

    def get_shot_document_by_string(self, string: str) -> dict[str, Any]:
        """Retrieve shot document from parsed string identifier.

        Parses the string using codex to extract fields, then queries the
        database for a matching shot.

        Args:
            string: Shot identifier string to parse and use for querying.

        Returns:
            Shot document dictionary with _id converted to string.

        Raises:
            ShotNotFoundError: If no shot matches the parsed string fields.
        """
        fields = codex.get_fields(string)
        return self.get_shot_document_by_fields(fields)

    def get_asset_tag_document_by_id(self, document_id: str) -> dict[str, Any]:
        """Retrieve asset tag document by ObjectId.

        Args:
            document_id: AssetTag document ID as string representation of ObjectId.

        Returns:
            AssetTag document dictionary with _id converted to string.

        Raises:
            AssetTagNotFoundError: If no asset with the given ID exists.
        """
        document = self.asset_tags.find_one(ObjectId(document_id))
        if not document:
            raise AssetTagNotFoundError(f'No asset tag with _id="{document_id}" was found')
        return self.stringify_id(document)

    def get_asset_tag_document_by_name(self, tag: str) -> dict[str, Any]:
        """Retrieve asset tag document by tag name.

        Args:
            tag: The asset tag name to search for.

        Returns:
            AssetTag document dictionary with _id converted to string.

        Raises:
            AssetTagNotFoundError: If no asset with the given name exists.
        """
        document = self.asset_tags.find_one({"tag": tag})
        if not document:
            raise AssetTagNotFoundError(f'No asset tag with tag="{tag}" was found')
        return self.stringify_id(document)

    def get_shot_tag_document_by_id(self, document_id: str) -> dict[str, Any]:
        """Retrieve shot tag document by ObjectId.

        Args:
            document_id: ShotTag document ID as string representation of ObjectId.

        Returns:
            ShotTag document dictionary with _id converted to string.

        Raises:
            ShotTagNotFoundError: If no shot with the given ID exists.
        """
        document = self.shot_tags.find_one(ObjectId(document_id))
        if not document:
            raise ShotTagNotFoundError(f'No shot tag with _id="{document_id}" was found')
        return self.stringify_id(document)

    def get_shot_tag_document_by_name(self, tag: str) -> dict[str, Any]:
        """Retrieve shot tag document by tag name.

        Args:
            tag: The shot tag name to search for.

        Returns:
            ShotTag document dictionary with _id converted to string.

        Raises:
            ShotTagNotFoundError: If no shot with the given name exists.
        """
        document = self.shot_tags.find_one({"tag": tag})
        if not document:
            raise ShotTagNotFoundError(f'No shot tag with tag="{tag}" was found')
        return self.stringify_id(document)

    def stringify_id(self, document: dict[str, Any]) -> dict[str, Any]:
        """Convert ObjectId to string in document's _id field.

        Modifies the document in-place to convert the MongoDB ObjectId to
        its string representation for JSON serialization and API responses.

        Args:
            document: MongoDB document containing an _id field with ObjectId.

        Returns:
            Same document reference with _id field converted to string.
        """
        document["_id"] = str(document["_id"])
        return document

    def start_local_mongodb_server(self) -> None:
        """Start local MongoDB server if not already running.

        Only executes if the server is configured as local (localhost or
        127.0.0.1). Starts the MongoDB daemon from BLUEPEPPER_ROOT/bin/mongodb
        and registers cleanup to terminate the process on exit.

        Raises:
            ConnectionFailure: If unable to connect to MongoDB after startup
                attempts, or if mongod executable is not found.
        """
        if not self.is_local_server:
            return

        # Skip if server already running
        if self.test_connection(0.02):
            logging.info("MongoDB Server is already running")
            return

        logging.info("Starting local MongoDB Server")
        root_dir = Path(os.environ["BLUEPEPPER_ROOT"])
        mongod_path = root_dir / "bin/mongodb/mongod.exe"
        db_path = root_dir.parent / ".database"
        db_path.mkdir(parents=True, exist_ok=True)

        command = [
            str(mongod_path),
            "--dbpath",
            str(db_path),
            "--port",
            str(self.settings.port),
        ]

        proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        register(lambda: proc.terminate() if proc.poll() is None else None)

        if not self.test_connection_retries(timeout_s=0.2, retries=20):
            msg = f"Failed to connect to MongoDB server {self.settings.host}:{self.settings.port}"
            raise errors.ConnectionFailure(msg)


database = BigMongoClient()

if __name__ == "__main__":
    doc = database.get_asset_document_by_string("D:/projects/myAwesomeProject/library/fx/dev00/dev00_v035.ma")
    print(doc)
