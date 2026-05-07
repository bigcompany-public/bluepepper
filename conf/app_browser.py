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
    modeling_workfile_kind = FileKind(
        name="asset_modeling_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_modeling_workfile_blender,
    )
    asset_modeling_task.add_kind(modeling_workfile_kind)

    # Surfacing
    asset_surfacing_task = Task("surfacing")
    asset_entity.add_task(asset_surfacing_task)
    surfacing_workfile_kind = FileKind(
        name="asset_surfacing_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_surfacing_workfile_blender,
    )
    asset_surfacing_task.add_kind(surfacing_workfile_kind)

    # rigging
    asset_rigging_task = Task("rigging")
    asset_entity.add_task(asset_rigging_task)
    rigging_workfile_kind = FileKind(
        name="asset_rigging_workfile_blender",
        label="Workfile (blender)",
        convention=codex.convs.asset_rigging_workfile_blender,
    )
    asset_rigging_task.add_kind(rigging_workfile_kind)

    # Shots
    shot_entity = Entity(name="shot", collection="shots", filters=["sequence"])
    config.add_entity(shot_entity)

    shot_layout_task = Task("layout")
    shot_entity.add_task(shot_layout_task)
    layout_workfile_kind = FileKind(
        name="shot_layout_workfile",
        label="Workfile",
        convention=codex.convs.shot_layout_workfile,
    )
    shot_layout_task.add_kind(layout_workfile_kind)

    shot_anim_task = Task("anim")
    shot_entity.add_task(shot_anim_task)
    anim_workfile_kind = FileKind(
        name="shot_anim_workfile",
        label="Workfile",
        convention=codex.convs.shot_anim_workfile,
    )
    shot_anim_task.add_kind(anim_workfile_kind)

    shot_lighting_task = Task("lighting")
    shot_entity.add_task(shot_lighting_task)
    lighting_workfile_kind = FileKind(
        name="shot_lighting_workfile",
        label="Workfile",
        convention=codex.convs.shot_lighting_workfile,
    )
    shot_lighting_task.add_kind(lighting_workfile_kind)

    # Global menu actions
    asset_document_help_me_action = MenuAction(
        label="Help Me",
        qta_icon="fa5s.hand-sparkles",
        module="bluepepper.tools.browser.browser_actions",
        function="asset_document_help_me",
        kwargs={"document": "<document>"},
        doc_filter=is_asset,
    )
    asset_add_tag_action = MenuAction(
        label="Add Tag",
        qta_icon="mdi.tag-plus",
        module="bluepepper.tools.browser.browser_actions",
        function="asset_add_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_asset,
        mode="all",
    )
    asset_remove_tag_action = MenuAction(
        label="Remove Tag",
        qta_icon="mdi.tag-minus",
        module="bluepepper.tools.browser.browser_actions",
        function="asset_remove_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_asset,
        mode="all",
    )
    shot_add_tag_action = MenuAction(
        label="Add Tag",
        qta_icon="mdi.tag-plus",
        module="bluepepper.tools.browser.browser_actions",
        function="shot_add_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_shot,
        mode="all",
    )
    shot_remove_tag_action = MenuAction(
        label="Remove Tag",
        qta_icon="mdi.tag-minus",
        module="bluepepper.tools.browser.browser_actions",
        function="shot_remove_tag",
        kwargs={"documents": "<documents>"},
        doc_filter=is_shot,
        mode="all",
    )
    shot_document_help_me_action = MenuAction(
        label="Help Me",
        qta_icon="fa5s.hand-sparkles",
        module="bluepepper.tools.browser.browser_actions",
        function="shot_document_help_me",
        kwargs={"document": "<document>"},
        doc_filter=is_shot,
    )
    copy_name_action = MenuAction(
        label="Copy Name",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="send_strings_to_clipboard",
        kwargs={"strings": "<document_names>"},
        mode="all",
    )
    asset_copy_identifier_action = MenuAction(
        label="Copy Identifier",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="asset_send_identifiers_to_clipboard",
        kwargs={"documents": "<documents>"},
        doc_filter=is_asset,
        mode="all",
    )
    copy_id_action = MenuAction(
        label="Copy ID",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="send_strings_to_clipboard",
        kwargs={"strings": "<document_ids>"},
        mode="all",
    )
    copy_doc_action = MenuAction(
        label="Copy Document",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="send_json_to_clipboard",
        kwargs={"serializable": "<documents>"},
        mode="all",
    )
    document_python_script_action = MenuAction(
        label="Execute Python Script",
        qta_icon="mdi6.language-python",
        module="bluepepper.tools.batcher.python_script_drop_dialog",
        function="add_jobs",
        kwargs={"browser": "<browser>", "targets": "<document_ids>"},
        mode="all",
    )
    asset_show_in_aquarium_action = MenuAction(
        label="Show in Aquarium",
        icon="aquarium.png",
        module="bluepepper.tools.browser.browser_actions",
        function="asset_show_in_aquarium",
        kwargs={"document": "<document>"},
        doc_filter=is_asset,
    )
    shot_show_in_aquarium_action = MenuAction(
        label="Show in Aquarium",
        icon="aquarium.png",
        module="bluepepper.tools.browser.browser_actions",
        function="shot_show_in_aquarium",
        kwargs={"document": "<document>"},
        doc_filter=is_shot,
    )
    shot_fetch_breakdownlist_action = MenuAction(
        label="Fetch Breakdownlist (from aquarium)",
        qta_icon="mdi.database-import-outline",
        module="bluepepper.tools.browser.browser_actions",
        function="shot_fetch_breakdownlist",
        kwargs={"document_id": "<document_id>"},
        doc_filter=is_shot,
    )
    kind_show_in_explorer_action = MenuAction(
        label="Show in explorer",
        qta_icon="fa6s.folder-open",
        module="bluepepper.tools.browser.browser_actions",
        function="kind_show_in_explorer",
        kwargs={"documents": "<documents>", "convention": "<convention>"},
        mode="all",
    )
    kind_copy_path_action = MenuAction(
        label="Copy Path",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="kind_copy_path",
        kwargs={"documents": "<documents>", "convention": "<convention>"},
        mode="all",
    )
    kind_copy_filename_action = MenuAction(
        label="Copy File Name",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="kind_copy_filename",
        kwargs={"documents": "<documents>", "convention": "<convention>"},
        mode="all",
    )
    file_copy_path_action = MenuAction(
        label="Copy Path",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="file_copy_paths",
        kwargs={"paths": "<paths>"},
        mode="all",
    )
    file_copy_filename_action = MenuAction(
        label="Copy File Name",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="file_copy_filename",
        kwargs={"paths": "<paths>"},
        mode="all",
    )
    file_copy_file_action = MenuAction(
        label="Copy File",
        qta_icon="fa5.clipboard",
        module="bluepepper.tools.browser.browser_actions",
        function="file_copy_file",
        kwargs={"paths": "<paths>"},
        mode="all",
    )
    file_show_in_explorer = MenuAction(
        label="Show in explorer",
        qta_icon="fa6s.folder-open",
        module="bluepepper.tools.browser.browser_actions",
        function="file_show_in_explorer",
        kwargs={"path": "<path>"},
    )
    file_increment_version = MenuAction(
        label="Increment",
        qta_icon="msc.versions",
        module="bluepepper.tools.browser.browser_actions",
        function="file_increment_version",
        kwargs={"path": "<path>", "convention": "<convention>", "description": "Incremented"},
    )
    file_open_in_vscode = MenuAction(
        label="Open in VSCode",
        qta_icon="msc.vscode",
        module="bluepepper.tools.browser.browser_actions",
        function="file_open_in_vscode",
        kwargs={"path": "<path>"},
        path_filter=is_text,
    )
    file_help_me_action = MenuAction(
        label="Help Me",
        qta_icon="fa5s.hand-sparkles",
        module="bluepepper.tools.browser.browser_actions",
        function="file_help_me",
        kwargs={"path": "<path>"},
    )
    file_python_script_action = MenuAction(
        label="Execute Python Script",
        qta_icon="mdi6.language-python",
        module="bluepepper.tools.batcher.python_script_drop_dialog",
        function="add_jobs",
        kwargs={"browser": "<browser>", "targets": "<paths>"},
        mode="all",
    )

    test_action = MenuAction(
        label="Test",
        module="sandbox",
        function="main",
        kwargs={
            "browser": "<browser>",
            "document": "<document>",
            "document_name": "<document_name>",
            "document_id": "<document_id>",
            "path": "<path>",
            "convention": "<convention>",
            "documents": "<documents>",
            "document_names": "<document_names>",
            "document_ids": "<document_ids>",
            "paths": "<paths>",
        },
    )

    for entity in config.entities.values():
        entity.add_document_action(test_action)
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
        entity.add_document_action(document_python_script_action)
        for task in entity.tasks.values():
            for kind in task.kinds.values():
                # Kind actions
                kind.add_kind_action(kind_show_in_explorer_action)
                kind.add_kind_action(kind_copy_path_action)
                kind.add_kind_action(kind_copy_filename_action)

                # File actions
                kind.add_file_action(test_action)
                kind.add_file_action(file_show_in_explorer)
                kind.add_file_action(file_copy_path_action)
                kind.add_file_action(file_copy_filename_action)
                kind.add_file_action(file_copy_file_action)
                kind.add_file_action(file_open_in_vscode)
                kind.add_file_action(file_increment_version)
                kind.add_file_action(file_help_me_action)
                kind.add_file_action(file_python_script_action)

    # More specific menu actions
    action = BatcherMenuAction(
        label="Build Workfile",
        job_name="Build Workfile - <document_name>",
        job_description="Copying empty blender file at the proper location for <document_name>",
        batcher_module="conf.scripts.example_build_modeling_workfile",
        batcher_function="main",
        batcher_kwargs={"document": "<document>"},
        batcher_notification=True,
        batcher_notification_message="<document_name> - New workfile was created",
    )
    modeling_workfile_kind.add_kind_action(action)

    return config
