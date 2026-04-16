import json
import logging
import shutil
from pathlib import Path
from typing import Any, List, Optional

from lucent import Convention

from bluepepper.clipboard import (
    clear_clipboard,
    send_paths_to_clipboard,
    send_text_to_clipboard,
)
from bluepepper.core import codex
from bluepepper.entities import Asset, Shot
from bluepepper.openfile import open_file, show_in_explorer
from bluepepper.softwares.vscode_launcher import VsCodeLauncher
from bluepepper.tools.helpme.helpme_widget import show_dialog as show_helpme_dialog
from bluepepper.tools.tags.tag_manager_widget import (
    show_asset_tag_manager_dialog,
    show_shot_tag_manager_dialog,
)


def asset_document_help_me(document: dict):
    show_helpme_dialog(asset_id=document["_id"])


def shot_document_help_me(document: dict):
    show_helpme_dialog(shot_id=document["_id"])


def asset_add_tag(documents: list[dict]):
    tag_documents = show_asset_tag_manager_dialog()
    if not tag_documents:  # Cancelled by the user
        return

    for document in documents:
        asset = Asset(document["_id"])
        for tag_document in tag_documents:
            asset.add_tag(tag=tag_document["tag"])


def asset_remove_tag(documents: list[dict]):
    tag_documents = show_asset_tag_manager_dialog()
    if not tag_documents:  # Cancelled by the user
        return

    for document in documents:
        asset = Asset(document["_id"])
        for tag_document in tag_documents:
            asset.remove_tag(tag=tag_document["tag"])


def shot_add_tag(documents: list[dict]):
    tag_documents = show_shot_tag_manager_dialog()
    if not tag_documents:  # Cancelled by the user
        return

    for document in documents:
        shot = Shot(document["_id"])
        for tag_document in tag_documents:
            shot.add_tag(tag=tag_document["tag"])


def shot_remove_tag(documents: list[dict]):
    tag_documents = show_shot_tag_manager_dialog()
    if not tag_documents:  # Cancelled by the user
        return

    for document in documents:
        shot = Shot(document["_id"])
        for tag_document in tag_documents:
            shot.remove_tag(tag=tag_document["tag"])


def file_help_me(path: Path):
    show_helpme_dialog(path=path)


def send_strings_to_clipboard(strings: list[str], separator: str = "\n"):
    if not strings:
        clear_clipboard()
        return
    send_text_to_clipboard(separator.join(strings))


def send_json_to_clipboard(serializable: Any, indent: int = 4):
    send_text_to_clipboard(json.dumps(serializable, indent=indent))


def asset_send_identifiers_to_clipboard(documents: list[dict[str, str]]):
    strings = [codex.convs.asset_identifier.format(doc) for doc in documents]
    send_strings_to_clipboard(strings)


def asset_show_in_aquarium(document: dict):
    aq_key = document.get("_aquariumKey")
    if not aq_key:
        return
    url = f"https://bigcompany.aquarium.app/apps/asseteditor?itemKeys={aq_key}"
    open_file(url)


def shot_show_in_aquarium(document: dict):
    aq_key = document.get("_aquariumKey")
    if not aq_key:
        return
    url = f"https://bigcompany.aquarium.app/apps/shoteditor?itemKeys={aq_key}"
    open_file(url)


def shot_fetch_breakdownlist(document_id: str):
    shot = Shot.from_document_id(document_id)
    shot.update_database_breakdown()


def kind_show_in_explorer(documents: List[dict], convention: Convention):
    # Get unique paths to reveal in explorer
    paths_to_show: List[Path] = []
    for document in documents:
        glob_pattern = Path(convention.glob_pattern(document))
        parts = []
        for part in glob_pattern.parts:
            if "*" in part:
                break
            parts.append(part)
        paths_to_show.append(Path("/".join(parts)))
    paths_to_show = list(set(paths_to_show))

    # Only open folders, not files
    for path in paths_to_show:
        if path.is_file():
            path = path.parent
        path.mkdir(exist_ok=True, parents=True)
        open_file(path)


def kind_copy_path(documents: List[dict], convention: Convention):
    strings = []
    for document in documents:
        strings.append(convention.human_readable_pattern(document))
    send_strings_to_clipboard(strings)


def kind_copy_filename(documents: List[dict], convention: Convention):
    strings = []
    for document in documents:
        strings.append(Path(convention.human_readable_pattern(document)).name)
    send_strings_to_clipboard(strings)


def file_copy_paths(paths: list[Path]):
    send_strings_to_clipboard([path.as_posix() for path in paths])


def file_copy_filename(paths: list[Path]):
    send_strings_to_clipboard([path.name for path in paths])


def file_copy_file(paths: list[Path]):
    send_paths_to_clipboard(paths)


def file_show_in_explorer(path: Path):
    show_in_explorer(path)


def file_increment_version(
    path: Path, convention: Convention, description: Optional[str] = None
):
    fields_to_enforce = {"description": description} if description else None
    dst = convention.increment(path, fields_to_enforce=fields_to_enforce)
    logging.info(f"Copying {path} to {dst}")
    shutil.copy(path, dst)


def file_open_in_vscode(path: Path):
    vscode = VsCodeLauncher(path)
    vscode.open()
