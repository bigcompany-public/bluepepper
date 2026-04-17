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

# TODO : add retries mechanisms with the tenacity package

_SOCKET_TIMEOUT_S = 0.5
_LOCAL_STARTUP_RETRIES = 20
_LOCAL_STARTUP_TIMEOUT_S = 0.2


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
    for assets and shots with robust error handling.

    Three connection modes are supported, configured via DatabaseSettings:
    - ``host-port``: connects to a remote/LAN server by hostname and port.
      A fast socket-level probe is run first so failures are detected quickly
      rather than waiting for PyMongo's own timeout.
    - ``uri``: connects using a full MongoDB URI string.
      Connection validation is delegated entirely to PyMongo
      (``serverSelectionTimeoutMS`` is set to 3 s).
    - ``local``: starts a ``mongod`` process on localhost if one is not already
      running, then connects to it.
    """

    def __init__(self) -> None:
        """Initialise the appropriate connection based on DatabaseSettings.mode.

        Raises:
            ValueError: If ``settings.mode`` is not one of the recognised modes.
            errors.ConnectionFailure: If the server cannot be reached after all
                attempts.
        """
        logging.info("Connecting to MongoDB database")
        logging.getLogger("pymongo").setLevel(logging.INFO)
        self.settings: DatabaseSettings = DatabaseSettings()

        if self.settings.mode == "host-port":
            self._init_host_port()
        elif self.settings.mode == "local":
            self._init_local()
        elif self.settings.mode == "uri":
            self._init_uri()
        else:
            raise ValueError(
                f'{self.settings.mode} is not a valid database mode. Choose one of: "host-port", "uri", "local".'
            )

    def _init_host_port(self) -> None:
        """Connect to a remote/LAN MongoDB server by host and port.

        A single socket-level probe is performed before handing control to
        PyMongo.  This gives a fast, deterministic failure rather than waiting
        for PyMongo's driver-level timeout, which can be unreliable at short
        durations.

        Raises:
            errors.ConnectionFailure: If the socket probe fails.
        """
        if not self._socket_reachable(self.settings.host, self.settings.port, _SOCKET_TIMEOUT_S):
            raise errors.ConnectionFailure(
                f"Cannot reach MongoDB server at {self.settings.host}:{self.settings.port} "
                f"(socket timeout {_SOCKET_TIMEOUT_S} s)"
            )
        super().__init__(
            self.settings.host,
            self.settings.port,
            username=self.settings.user,
            password=self.settings.password,
        )

    def _init_uri(self) -> None:
        """Connect using a full MongoDB URI string.

        PyMongo handles all connection details; ``serverSelectionTimeoutMS``
        is set to 3 000 ms so failures surface quickly without a socket probe
        (host/port may not be straightforwardly parseable from an arbitrary URI).

        Raises:
            errors.ConnectionFailure: If PyMongo cannot select a server within
                the timeout.
        """
        super().__init__(self.settings.uri, serverSelectionTimeoutMS=3_000)
        # Force a round-trip so the caller gets a ConnectionFailure immediately
        # rather than on the first actual query.
        try:
            self.admin.command("ping")
        except errors.ConnectionFailure:
            raise
        except Exception as exc:
            raise errors.ConnectionFailure(str(exc)) from exc

    def _init_local(self) -> None:
        """Ensure a local ``mongod`` is running, then connect.

        If no server is detected on 127.0.0.1:27017 a new ``mongod`` process
        is spawned.  The startup loop already confirms reachability, so no
        further probe is needed after ``super().__init__``.

        Raises:
            errors.ConnectionFailure: If ``mongod`` cannot be started or does
                not become reachable within the retry window.
        """
        self._ensure_local_mongodb_running()
        super().__init__(host="127.0.0.1", port=27017)

    @staticmethod
    def _socket_reachable(host: str, port: int, timeout_s: float) -> bool:
        """Return True if a TCP connection to *host*:*port* succeeds.

        PyMongo's own timeout is unreliable at sub-second values because it
        operates at the driver level rather than at the OS socket level.  This
        method performs a plain TCP probe so failures are detected within the
        specified *timeout_s*.

        Args:
            host: Hostname or IP address to connect to.
            port: TCP port number.
            timeout_s: Seconds to wait before declaring the host unreachable.

        Returns:
            ``True`` if the connection succeeded, ``False`` otherwise.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout_s)
        try:
            sock.connect((host, port))
            sock.shutdown(socket.SHUT_RDWR)
            return True
        except (OSError, socket.timeout):
            return False
        finally:
            sock.close()

    def _ensure_local_mongodb_running(self) -> None:
        """Start a local ``mongod`` process if one is not already running.

        The database files are stored in a ``.database`` directory located
        next to ``BLUEPEPPER_ROOT``.  The ``mongod`` executable is expected at
        ``$BLUEPEPPER_ROOT/bin/mongodb/mongod.exe``.

        The spawned process is registered for automatic termination on
        interpreter exit.

        Raises:
            errors.ConnectionFailure: If ``mongod`` does not become reachable
                within ``_LOCAL_STARTUP_RETRIES`` attempts.
        """
        if self._socket_reachable("127.0.0.1", 27017, timeout_s=0.05):
            logging.info("Local MongoDB server is already running")
            return

        logging.info("Starting local MongoDB server")
        root_dir = Path(os.environ["BLUEPEPPER_ROOT"])
        mongod_path = root_dir / "bin/mongodb/mongod.exe"
        db_path = root_dir.parent / ".database"
        db_path.mkdir(parents=True, exist_ok=True)

        command = [str(mongod_path), "--dbpath", str(db_path), "--port", "27017"]
        proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        register(lambda: proc.terminate() if proc.poll() is None else None)

        for attempt in range(1, _LOCAL_STARTUP_RETRIES + 1):
            logging.debug(f"Waiting for local mongod (attempt {attempt}/{_LOCAL_STARTUP_RETRIES})")
            if self._socket_reachable("127.0.0.1", 27017, _LOCAL_STARTUP_TIMEOUT_S):
                logging.info("Local MongoDB server is ready")
                return

        raise errors.ConnectionFailure(f"Local mongod did not become reachable after {_LOCAL_STARTUP_RETRIES} attempts")

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
        """Check if MongoDB server is configured as local."""
        return self.settings.mode == "local"

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
            AssetTagNotFoundError: If no asset tag with the given ID exists.
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
            AssetTagNotFoundError: If no asset tag with the given name exists.
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
            ShotTagNotFoundError: If no shot tag with the given ID exists.
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
            ShotTagNotFoundError: If no shot tag with the given name exists.
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


database = BigMongoClient()

if __name__ == "__main__":
    doc = database.get_asset_document_by_string("D:/projects/myAwesomeProject/library/fx/dev00/dev00_v035.ma")
    print(doc)
