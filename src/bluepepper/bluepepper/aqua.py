from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Optional

import keyring
from aquarium import Aquarium
from aquarium.aquarium import Asset, Element, Item, Project, Shot, Task
from aquarium.exceptions import AutorisationError
from conf.aquarium import AquariumConfig

from bluepepper.core import codex, init_logging
from bluepepper.helpers.timeit import timeit

# TODO : ajouter des retries avec le package "tenacity"


BLUEPEPPER_AQUARIUM_KEYRING = "bluepepper_aquarium"

# Create an Aqua instance at the module level to avoid re-connecting again and again
aqua: Optional[Aqua] = None


@timeit
def get_aqua() -> Aqua:
    """Get or create the global Aqua instance."""
    global aqua
    if aqua is None:
        connect()
    return aqua


class AquaPermissionError(Exception): ...


class AquaProjectNotFoundError(Exception): ...


class AquaAssetNotFoundError(Exception): ...


class AquaShotNotFoundError(Exception): ...


class AquaTaskNotFoundError(Exception): ...


class Aqua:
    def __init__(self, aq: Aquarium):
        self.aq = aq
        self._test_connection()
        self.project: Project = self._test_project_permissions()
        logging.info("Connection to aquarium was successful")

    @timeit
    def _test_connection(self) -> Project | None:
        user = self.aq.get_current_user()
        if user.data.get("email", None) or user.data.get("name"):
            return
        raise ConnectionError("Failed to connect to aquarium")

    @timeit
    def _test_project_permissions(self):
        query = f"# item.type == 'Project' AND item.data.name == '{AquariumConfig.project}' UNIQUE"
        result = self.aq.query(query)
        if not result:
            raise AquaProjectNotFoundError(f'Aquarium Project not found : "{AquariumConfig.project}"')

        project: Project = self.aq.project(int(result[0]["_key"])).get()
        if not project:
            raise AquaPermissionError(f"Current user doesn't have access to project : {AquariumConfig.project}")
        return project

    def ensure_hierarchy(self, path: Path, color: str = "") -> Item:
        path = Path(path)
        current_item: Item = self.project
        for subdir in path.parts:
            result: list[Element] = current_item.get_children(types="Group", names=subdir)

            # Create subfolder if it doesn't exist
            if not result:
                logging.info("Creating subfolder {}".format(subdir))
                data = {"name": subdir}
                if color:
                    data["labelColor"] = color
                current_item = current_item.append(
                    type="Group",
                    data=data,
                    edge_type="Child",
                    edge_data={},
                    apply_template=False,
                ).item

            # If the subfolder exists, it becomes the next item to look into
            else:
                current_item = result[0].item
        return current_item

    def get_asset_path(self, fields: dict[str, str]) -> Path:
        return Path(codex.convs.aquarium_asset.format(fields))

    def ensure_asset_hierarchy(self, path: Path) -> Item:
        return self.ensure_hierarchy(path, AquariumConfig.asset_color)

    def create_asset(self, fields: dict[str, str]) -> Asset:
        logging.info(f"Creating aquarium asset : {fields}")
        group_path = self.get_asset_path(fields).parent
        group = self.ensure_asset_hierarchy(group_path)
        data = fields.copy()
        data["name"] = fields["asset"]
        template: int = AquariumConfig.asset_templates.get(fields["type"])
        if not template:
            template = AquariumConfig.asset_templates["_default"]

        # Raise error if asset already exists
        result = group.get_children(types="Asset", names=fields["asset"])
        if result:
            raise RuntimeError(f"The asset already exists : {fields['asset']}")

        element: Element = group.append(
            type="Asset",
            data=data,
            edge_type="Child",
            edge_data={},
            apply_template=True,
            template_key=str(template),
        )
        return element.item

    def get_asset_from_fields(self, fields: dict[str, str]) -> Asset:
        path = self.get_asset_path(fields)
        return self.get_asset_from_path(path)

    @timeit
    def get_asset_from_path(self, path: Path) -> Asset:
        path = Path(path)
        current_item = self.project

        # Traverse group hierarchy
        for subdir in path.parts[:-1]:
            result = current_item.get_children(types="Group", names=subdir)
            if not result:
                raise AquaAssetNotFoundError(f"Asset not found on aquarium : {path}")
            current_item = result[0].item

        # Return asset item
        fields = codex.convs.aquarium_asset.parse(path)
        result = current_item.get_children(types="Asset", names=fields["asset"])
        if not result:
            raise AquaAssetNotFoundError(f"Asset not found on aquarium : {path}")
        return result[0].item

    def get_asset_from_key(self, key: int) -> Asset:
        try:
            item = self.aq.item(int(key)).get()
        except AutorisationError:
            raise AquaAssetNotFoundError(f"Asset not found on aquarium : {key}")
        return item

    @timeit
    def get_asset_task(self, asset: Asset, task: str) -> Task:
        result = asset.get_tasks(task_name=task)
        if not result:
            raise AquaTaskNotFoundError(f"Task not found on aquarium : {asset.data['name']}/{task}")
        return result[0]

    def create_shot(self, fields: dict[str, str]) -> Shot:
        logging.info(f"Creating aquarium shot : {fields}")
        group_path = self.get_shot_path(fields).parent
        group = self.ensure_shot_hierarchy(group_path)
        data = fields.copy()
        data["name"] = fields["shot"]
        template: int = AquariumConfig.shot_template

        # Raise error if shot already exists
        result = group.get_children(types="Shot", names=fields["shot"])
        if result:
            raise RuntimeError(f"The shot already exists : {fields['shot']}")

        element: Element = group.append(
            type="Shot",
            data=data,
            edge_type="Child",
            edge_data={},
            apply_template=True,
            template_key=str(template),
        )
        return element.item

    def get_shot_path(self, fields: dict[str, str]) -> Path:
        return Path(codex.convs.aquarium_shot.format(fields))

    def ensure_shot_hierarchy(self, path: Path) -> Item:
        return self.ensure_hierarchy(path, AquariumConfig.shot_color)

    def get_shot_from_key(self, key: int) -> Shot:
        try:
            item = self.aq.item(int(key)).get()
        except AutorisationError:
            raise AquaShotNotFoundError(f"Shot not found on aquarium : {key}")
        return item


def connect_with_credentials(email: str, password: str, store: bool = False) -> Aqua:
    aq = Aquarium(api_url=AquariumConfig.url)
    logging.info(f"Logging with credentials : {email} // **********")
    aq.connect(email=email, password=password)
    if store:
        store_credentials(email=email, password=password)
    global aqua
    aqua = Aqua(aq=aq)
    return aqua


def connect_with_token(token: str) -> Aqua:
    """
    Connection with tokens is designed for the render farm, or other places where providing
    plain text credentials is dangerous.
    As tokens become stale with time, users should use connect_with_credentials() on a day-to-day basis
    """
    aq = Aquarium(api_url=AquariumConfig.url, token=token)
    hidden_token = token[:5] + "*****************" + token[-5:]
    logging.info(f"Logging with token: {hidden_token}")
    global aqua
    aqua = Aqua(aq=aq)
    return aqua


def connect_with_bot() -> Aqua:
    logging.info("Logging to Aquarium as Bot")
    aq = Aquarium(api_url=AquariumConfig.url)
    aq.bot(AquariumConfig.bot_key).signin(AquariumConfig.bot_secret)
    global aqua
    aqua = Aqua(aq=aq)
    return aqua


@timeit
def user_has_stored_credentials() -> bool:
    creds = keyring.get_credential(BLUEPEPPER_AQUARIUM_KEYRING, None)
    return bool(creds)


def connect_with_stored_credentials() -> Aqua:
    logging.info("Fetching stored credentials")
    creds = keyring.get_credential(service_name=BLUEPEPPER_AQUARIUM_KEYRING, username=None)
    return connect_with_credentials(email=creds.username, password=creds.password)


@timeit
def connect(email: str = "", password: str = "", token="", bot: bool = True, store: bool = False) -> Aqua:
    logging.info("Connecting to Aquarium")
    if token:
        connect_with_token(token)
    elif email and password:
        connect_with_credentials(email=email, password=password, store=store)
    elif os.environ.get("BLUEPEPPER_AQUARIUM_TOKEN"):
        connect_with_token(os.environ.get("BLUEPEPPER_AQUARIUM_TOKEN"))
    elif user_has_stored_credentials():
        connect_with_stored_credentials()
    elif bot:
        connect_with_bot()
    else:
        raise ConnectionError(
            "Please provide a way to connect to aquarium (credentials, token, environment_variable...)"
        )


@timeit
def store_credentials(email: str, password: str) -> None:
    logging.info(f"Storing credentials : {email} // *********")
    keyring.set_password(service_name=BLUEPEPPER_AQUARIUM_KEYRING, username=email, password=password)


def clear_stored_credentials():
    creds = keyring.get_credential(BLUEPEPPER_AQUARIUM_KEYRING, None)
    if not creds:
        return
    logging.info("Clearing aquarium stored credentials")
    keyring.delete_password(BLUEPEPPER_AQUARIUM_KEYRING, creds.username)


def _main():
    init_logging("aquarium")
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", required=False, type=str, help="Email adress used to login")
    parser.add_argument("-p", "--password", required=False, type=str, help="Password")
    parser.add_argument("-t", "--token", required=False, type=str, help="Aquarium connexion token")
    parser.add_argument(
        "-nb",
        "--no_bot",
        action="store_true",
        help="Disable the option to connect as bot",
    )
    parser.add_argument(
        "-et",
        "--env_token",
        required=False,
        type=str,
        help="Aquarium connexion token to pass as an environment variable",
    )
    parser.add_argument(
        "-sc",
        "--store_credentials",
        action="store_true",
        help="Store user/password using keyring",
    )
    parser.add_argument(
        "-cc",
        "--clear_credentials",
        action="store_true",
        help="Clear user/password keyring entry",
    )

    args = parser.parse_args()

    if args.clear_credentials:
        clear_stored_credentials()

    if args.env_token:
        os.environ["BLUEPEPPER_AQUARIUM_TOKEN"] = args.env_token

    connect(
        email=args.email,
        password=args.password,
        token=args.token,
        store=args.store_credentials,
        bot=not args.no_bot,
    )


if __name__ == "__main__":
    # os.environ["BLUEPEPPER_TIMEIT"] = "1"
    _main()
