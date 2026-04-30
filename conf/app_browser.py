from pathlib import Path

from bluepepper.core import codex
from bluepepper.tools.browser.browser_config import AppConfig, BatcherMenuAction, Entity, FileKind, MenuAction, Task
from conf.project import ProjectSettings

PROJECT_SETTINGS = ProjectSettings()


def is_chr(doc: dict) -> bool:
    if not is_asset(doc):
        return False
    return doc["type"] == "chr"


def is_prp(doc: dict) -> bool:
    if not is_asset(doc):
        return False
    return doc["type"] == "prp"


def is_asset(doc: dict) -> bool:
    return bool(doc.get("asset"))


def is_shot(doc: dict) -> bool:
    return bool(doc.get("shot"))


def is_text(path: Path) -> bool:
    text_extensions = [".txt", ".ma", ".json", ".xstage"]
    return path.suffix in text_extensions


def is_binary(path: Path) -> bool:
    return not is_text(path)


def is_aquarium_available() -> bool:
    return "aquarium" in PROJECT_SETTINGS.production_trackers


def get_tool_config() -> AppConfig:
    config = AppConfig("bigBrowserMainApp")

    # Assets
    asset_entity = Entity(name="asset", collection="assets", filters=["type"])
    config.add_entity(asset_entity)

    # Modeling
    asset_modeling_task = Task("modeling")
    asset_entity.add_task(asset_modeling_task)
    kind = FileKind(
        name="asset_modeling_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_modeling_workfile_blender,
    )
    asset_modeling_task.add_kind(kind)

    # Surfacing
    asset_surfacing_task = Task("surfacing")
    asset_entity.add_task(asset_surfacing_task)
    kind = FileKind(
        name="asset_surfacing_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_surfacing_workfile_blender,
    )
    asset_surfacing_task.add_kind(kind)

    # texturing
    asset_texturing_task = Task("texturing")
    asset_entity.add_task(asset_texturing_task)
    kind = FileKind(
        name="asset_texturing_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_texturing_workfile_blender,
    )
    asset_texturing_task.add_kind(kind)

    # rigging
    asset_rigging_task = Task("rigging")
    asset_entity.add_task(asset_rigging_task)
    kind = FileKind(
        name="asset_rigging_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_rigging_workfile_blender,
    )
    asset_rigging_task.add_kind(kind)

    # grooming
    asset_grooming_task = Task("grooming")
    asset_entity.add_task(asset_grooming_task)
    kind = FileKind(
        name="asset_grooming_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_grooming_workfile_blender,
    )
    asset_grooming_task.add_kind(kind)

    # fx
    asset_fx_task = Task("fx")
    asset_entity.add_task(asset_fx_task)
    kind = FileKind(
        name="asset_fx_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_fx_workfile_blender,
    )
    asset_fx_task.add_kind(kind)

    # assembly
    asset_assembly_task = Task("assembly")
    asset_entity.add_task(asset_assembly_task)
    kind = FileKind(
        name="asset_assembly_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_assembly_workfile_blender,
    )
    asset_assembly_task.add_kind(kind)

    # Shots
    shot_entity = Entity(name="shot", collection="shots", filters=["season", "episode", "sequence"])
    config.add_entity(shot_entity)
    shot_layout_task = Task("layout")
    shot_entity.add_task(shot_layout_task)
    kind = FileKind(
        name="shot_layout_workfile",
        label="Workfile",
        convention=codex.convs.shot_layout_workfile,
    )
    shot_layout_task.add_kind(kind)

    # Global menu actions
    asset_document_help_me_action = MenuAction(
        label="Help Me",
        qta_icon="fa5s.hand-sparkles",
        module="bluepepper.tools.browser.browser_actions",
        callable="asset_document_help_me",
        kwargs={"document": "<document>"},
        doc_filter=is_asset,
    )
    asset_add_tag_action = MenuAction(
        label="Add Tag",
        qta_icon="mdi.tag-plus",
        module="bluepepper.tools.browser.browser_actions",
        callable="asset_add_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_asset,
    )
    asset_remove_tag_action = MenuAction(
        label="Remove Tag",
        qta_icon="mdi.tag-minus",
        module="bluepepper.tools.browser.browser_actions",
        callable="asset_remove_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_asset,
    )
    shot_add_tag_action = MenuAction(
        label="Add Tag",
        qta_icon="mdi.tag-plus",
        module="bluepepper.tools.browser.browser_actions",
        callable="shot_add_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_shot,
    )
    shot_remove_tag_action = MenuAction(
        label="Remove Tag",
        qta_icon="mdi.tag-minus",
        module="bluepepper.tools.browser.browser_actions",
        callable="shot_remove_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_shot,
    )
    shot_document_help_me_action = MenuAction(
        label="Help Me",
        qta_icon="fa5s.hand-sparkles",
        module="bluepepper.tools.browser.browser_actions",
        callable="shot_document_help_me",
        kwargs={"document": "<document>"},
        doc_filter=is_shot,
    )
    copy_name_action = MenuAction(
        label="Copy Name",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="send_strings_to_clipboard",
        kwargs={"strings": "<document_names>"},
    )
    asset_copy_identifier_action = MenuAction(
        label="Copy Identifier",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="asset_send_identifiers_to_clipboard",
        kwargs={"documents": "<documents>"},
        doc_filter=is_asset,
    )
    copy_id_action = MenuAction(
        label="Copy ID",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="send_strings_to_clipboard",
        kwargs={"strings": "<document_ids>"},
    )
    copy_doc_action = MenuAction(
        label="Copy Document",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="send_json_to_clipboard",
        kwargs={"serializable": "<documents>"},
    )
    asset_show_in_aquarium_action = MenuAction(
        label="Show in Aquarium",
        icon="aquarium.png",
        module="bluepepper.tools.browser.browser_actions",
        callable="asset_show_in_aquarium",
        kwargs={"document": "<document>"},
        doc_filter=is_asset,
    )
    shot_show_in_aquarium_action = MenuAction(
        label="Show in Aquarium",
        icon="aquarium.png",
        module="bluepepper.tools.browser.browser_actions",
        callable="shot_show_in_aquarium",
        kwargs={"document": "<document>"},
        doc_filter=is_shot,
    )
    shot_fetch_breakdownlist_action = MenuAction(
        label="Fetch Breakdownlist (from aquarium)",
        qta_icon="mdi.database-import-outline",
        module="bluepepper.tools.browser.browser_actions",
        callable="shot_fetch_breakdownlist",
        kwargs={"document_id": "<document_id>"},
        doc_filter=is_shot,
    )
    kind_show_in_explorer_action = MenuAction(
        label="Show in explorer",
        qta_icon="fa6s.folder-open",
        module="bluepepper.tools.browser.browser_actions",
        callable="kind_show_in_explorer",
        kwargs={"documents": "<documents>", "convention": "<convention>"},
    )
    kind_copy_path_action = MenuAction(
        label="Copy Path",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="kind_copy_path",
        kwargs={"documents": "<documents>", "convention": "<convention>"},
    )
    kind_copy_filename_action = MenuAction(
        label="Copy File Name",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="kind_copy_filename",
        kwargs={"documents": "<documents>", "convention": "<convention>"},
    )
    file_copy_path_action = MenuAction(
        label="Copy Path",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="file_copy_paths",
        kwargs={"paths": "<paths>"},
    )
    file_copy_filename_action = MenuAction(
        label="Copy File Name",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="file_copy_filename",
        kwargs={"paths": "<paths>"},
    )
    file_copy_file_action = MenuAction(
        label="Copy File",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        callable="file_copy_file",
        kwargs={"paths": "<paths>"},
    )
    file_show_in_explorer = MenuAction(
        label="Show in explorer",
        qta_icon="fa6s.folder-open",
        module="bluepepper.tools.browser.browser_actions",
        callable="file_show_in_explorer",
        kwargs={"path": "<path>"},
    )
    file_increment_version = MenuAction(
        label="Increment",
        qta_icon="msc.versions",
        module="bluepepper.tools.browser.browser_actions",
        callable="file_increment_version",
        kwargs={"path": "<path>", "convention": "<convention>", "description": "YOLO"},
    )
    file_open_in_vscode = MenuAction(
        label="Open in VSCode",
        qta_icon="msc.vscode",
        module="bluepepper.tools.browser.browser_actions",
        callable="file_open_in_vscode",
        kwargs={"path": "<path>"},
        path_filter=is_text,
    )
    file_help_me_action = MenuAction(
        label="Help Me",
        qta_icon="fa5s.hand-sparkles",
        module="bluepepper.tools.browser.browser_actions",
        callable="file_help_me",
        kwargs={"path": "<path>"},
    )
    placeholder_job_action = BatcherMenuAction(
        label="Create Batcher Job",
        job_name="Demo Batcher - <document_names>",
        job_description="Just doing stuff on <document_names>",
        batcher_module="bluepepper.tools.batcher.demo_script",
        batcher_function="main",
        batcher_kwargs={"some_arg": "<document_names>"},
    )

    for entity in config.entities.values():
        entity.add_document_action(placeholder_job_action)
        entity.add_document_action(copy_name_action)
        entity.add_document_action(asset_copy_identifier_action)
        entity.add_document_action(copy_id_action)
        entity.add_document_action(copy_doc_action)
        if is_aquarium_available():
            entity.add_document_action(asset_show_in_aquarium_action)
        entity.add_document_action(asset_document_help_me_action)
        entity.add_document_action(asset_add_tag_action)
        entity.add_document_action(asset_remove_tag_action)
        if is_aquarium_available():
            entity.add_document_action(shot_show_in_aquarium_action)
        entity.add_document_action(shot_fetch_breakdownlist_action)
        entity.add_document_action(shot_document_help_me_action)
        entity.add_document_action(shot_add_tag_action)
        entity.add_document_action(shot_remove_tag_action)
        for task in entity.tasks.values():
            for kind in task.kinds.values():
                # Kind actions
                kind.add_kind_action(kind_show_in_explorer_action)
                kind.add_kind_action(kind_copy_path_action)
                kind.add_kind_action(kind_copy_filename_action)

                # File actions
                kind.add_file_action(file_show_in_explorer)
                kind.add_file_action(file_copy_path_action)
                kind.add_file_action(file_copy_filename_action)
                kind.add_file_action(file_copy_file_action)
                kind.add_file_action(file_open_in_vscode)
                kind.add_file_action(file_increment_version)
                kind.add_file_action(file_help_me_action)

    return config
