"""
Example BigBrowser configuration for a 3D animation studio pipeline.

Demonstrates hierarchical configuration using Asset and Shot entities
with their respective workflows and tasks.
"""

from bluepepper.core import codex
from bluepepper.tools.browser.browser_config import (
    AppConfig,
    Entity,
    Kind,
    MenuAction,
    Task,
)

config = AppConfig("bigBrowserDemo")


def is_chr(doc: dict):
    return doc["type"] == "chr"


# Assets
asset_entity = Entity(name="asset", collection="assets", filters=["type"])
config.add_entity(asset_entity)
asset_copy_name_action = MenuAction(
    label="Copy Name",
    qta_icon="fa5.clipboard",
    module="bluepepper.tools.browser.browser_actions",
    callable="send_strings_to_clipboard",
    kwargs={"strings": "<document_names>"},
)
asset_copy_id_action = MenuAction(
    label="Copy ID",
    qta_icon="fa5.clipboard",
    module="bluepepper.tools.browser.browser_actions",
    callable="send_strings_to_clipboard",
    kwargs={"strings": "<document_ids>"},
)
asset_copy_doc_action = MenuAction(
    label="Copy Document",
    qta_icon="fa5.clipboard",
    module="bluepepper.tools.browser.browser_actions",
    callable="send_json_to_clipboard",
    kwargs={"serializable": "<documents>"},
)
show_in_aquarium_action = MenuAction(
    label="Show in Aquarium",
    icon="aquarium.png",
    module="bluepepper.tools.browser.browser_actions",
    callable="show_in_aquarium",
    kwargs={"document": "<document>"},
)
asset_entity.add_document_action(asset_copy_name_action)
asset_entity.add_document_action(asset_copy_id_action)
asset_entity.add_document_action(asset_copy_doc_action)
asset_entity.add_document_action(show_in_aquarium_action)

asset_modeling_task = Task("modeling", task_field="mdl")
asset_entity.add_task(asset_modeling_task)

asset_workfile_kind = Kind(name="workfile", convention=codex.convs.asset_maya_file)
asset_workfile_kind.add_file_action(
    MenuAction("Reveal in explorer", module="bluepepper.do_stuff", callable="do_stuff")
)
asset_workfile_kind.add_kind_action(
    MenuAction("Reveal in explorer", module="bluepepper.do_stuff", callable="do_stuff")
)
asset_dir_kind = Kind(
    name="asset_dir", label="Folder", convention=codex.convs.asset_dir
)
asset_publish_kind = Kind(
    name="asset_publish_file",
    label="Publish",
    convention=codex.convs.asset_publish_file,
)
asset_modeling_task.add_kind(asset_dir_kind)
asset_modeling_task.add_kind(asset_workfile_kind)
asset_modeling_task.add_kind(asset_publish_kind)

asset_surfacing_task = Task("surfacing", task_field="sur", filter=is_chr)
asset_entity.add_task(asset_surfacing_task)
asset_surfacing_task.add_kind(asset_dir_kind)

# Shots
shot_entity = Entity(
    name="shot", collection="shots", filters=["season", "episode", "sequence"]
)
config.add_entity(shot_entity)

shot_layout_task = Task("layout", task_field="lay")
shot_entity.add_task(shot_layout_task)

kind = Kind(name="workfile", convention=codex.convs.asset_maya_file)
kind.add_file_action(
    MenuAction("Reveal in explorer", module="bluepepper.do_stuff", callable="do_stuff")
)
kind.add_kind_action(
    MenuAction("Reveal in explorer", module="bluepepper.do_stuff", callable="do_stuff")
)
shot_layout_task.add_kind(kind)

if __name__ == "__main__":
    print(config.human_readable())
