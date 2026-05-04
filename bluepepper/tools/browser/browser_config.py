"""
Application configuration module using dataclasses.

This module defines a hierarchical configuration structure for the BigBrowser application,
providing type-safe access to entities, workflows, tasks, and their associated actions.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from lucent import Convention

from bluepepper.gui.utils import get_theme


@dataclass
class MenuAction:
    """
    Represents a menu action that can be triggered on kinds or files.

    Attributes:
        label: Display label for the menu action
        module: Python module path containing the callable
        callable: Function name to execute
        kwargs: Additional keyword arguments to pass to the callable
    """

    label: str
    module: str
    callable: str
    icon: str = field(default="")
    qta_icon: str = field(default="")
    qta_icon_color: str = field(default=get_theme()["icon_color"])
    kwargs: dict = field(default_factory=dict)
    mode: str = field(default="each")
    doc_filter: Callable[..., bool] | None = None
    path_filter: Callable[..., bool] | None = None

    def __post_init__(self):
        if self.mode not in {"all", "each"}:
            raise ValueError('MenuAction mode must be "all" or "each"')


@dataclass
class BatcherMenuAction(MenuAction):
    job_name: str = ""
    job_description: str = ""

    # Disable attributes that should be locked in this subclass
    module: str = field(default="bluepepper.tools.batcher.browser_connector", init=False)
    callable: str = field(default="add_job", init=False)
    kwargs: dict = field(default_factory=dict, init=False)
    mode: str = field(default="each")
    qta_icon: str = field(default="mdi6.factory")
    batcher_module: str = ""
    batcher_function: str = ""
    batcher_kwargs: dict = field(default_factory=dict)
    batcher_script: Path | None = None
    batcher_script_args: list[str] = field(default_factory=list[str])
    batcher_priority: int = 50
    batcher_notify_me_when_done: bool = False

    def __post_init__(self):
        if not self.job_name:
            raise AttributeError("Please provide a job name")
        if not self.job_description:
            raise AttributeError("Please provide a description")
        if not self.batcher_script and not self.batcher_module:
            raise AttributeError("A Batcher Job needs at least a script or a module")
        if self.batcher_module and not self.batcher_function:
            raise AttributeError("Please provide a function to execute")

        # special_keywords = ...

        self.kwargs = {
            "name": self.job_name,
            "description": self.job_description,
            "script_path": self.batcher_script,
            "script_args": self.batcher_script_args,
            "module": self.batcher_module,
            "function": self.batcher_function,
            "kwargs": self.batcher_kwargs,
            "priority": self.batcher_priority,
            "notify_when_done": self.batcher_notify_me_when_done,
            "browser": "<browser>",  # Needed by the add_job function, and must be resolved when triggering the action
        }

        super().__post_init__()


@dataclass
class FileKind:
    """
    Represents an kind within a workflow task (e.g., asset directory, file).

    Attributes:
        label: Display label for the kind
        template: Template identifier used for path resolution
        kind_menu_actions: Actions available in the kind's context menu
        file_menu_actions: Actions available for files within this kind
    """

    name: str
    convention: Convention
    label: str = field(default="")
    kind_actions: list[MenuAction] = field(default_factory=list[MenuAction])
    file_actions: list[MenuAction] = field(default_factory=list[MenuAction])

    def __post_init__(self):
        if not self.label:
            self.label = self.name.capitalize()

    def add_kind_action(self, action: MenuAction):
        self.kind_actions.append(action)

    def add_file_action(self, action: MenuAction):
        self.file_actions.append(action)


@dataclass
class Task:
    """
    Represents a task within a workflow (e.g., modeling, rigging).

    Attributes:
        label: Display label for the task
        kinds: Dictionary of workflow kinds, keyed by kind identifier
    """

    name: str
    task_field: str = field(default="")
    label: str = field(default="")
    kinds: dict[str, FileKind] = field(default_factory=dict[str, FileKind])
    doc_filter: Callable[..., bool] | None = None

    def __post_init__(self):
        if not self.label:
            self.label = self.name.capitalize()

    def add_kind(self, kind: FileKind):
        if kind.name in self.kinds:
            raise RuntimeError(f'Cannot add kind with name "{kind.name}". Name is already used')
        self.kinds[kind.name] = kind


@dataclass
class Entity:
    """
    Represents an entity type in the application (e.g., asset, shot, sequence).

    Attributes:
        database_collection: MongoDB/database collection name for this entity
        filters: List of available filter fields for querying
        workflows: Dictionary of workflows, keyed by workflow name
                  (_default is the fallback workflow)
    """

    name: str
    collection: str
    label: str = field(default="")
    filters: list[str] = field(default_factory=list[str])
    tasks: dict[str, Task] = field(default_factory=dict[str, Task])
    document_actions: list[MenuAction] = field(default_factory=list[MenuAction])

    def __post_init__(self):
        if not self.label:
            self.label = self.name.capitalize()

    def add_task(self, task: Task):
        if task.name in self.tasks:
            raise RuntimeError(f'Cannot add task with name "{task.name}". Name is already used')
        self.tasks[task.name] = task

    def add_document_action(self, action: MenuAction):
        self.document_actions.append(action)


@dataclass
class AppConfig:
    """
    Root application configuration.

    Attributes:
        app_name: Name of the application
        entities: Dictionary of entity configurations, keyed by entity type
    """

    name: str
    entities: dict[str, Entity] = field(default_factory=dict[str, Entity])

    def add_entity(self, entity: Entity):
        if entity.name in self.entities:
            raise RuntimeError(f'Cannot add entity with name "{entity.name}". Name is already used')
        self.entities[entity.name] = entity

    def human_readable(self) -> str:
        lines: list[str] = []
        lines += [f'BigBrowser "{self.name}"', ""]

        for _, entity in self.entities.items():
            lines.append("[Entity] " + entity.label)
            for _, task in entity.tasks.items():
                lines.append("    [Task] " + task.label)
                for _, kind in task.kinds.items():
                    lines.append("      [FileKind] " + kind.label)
                    for action in kind.kind_actions:
                        kwargs = ", ".join(f"{k}={v}" for k, v in action.kwargs.values())
                        lines.append(
                            f"        [FileKind Action] {action.label} -> {action.module}.{action.callable}({kwargs})"
                        )
                    for action in kind.file_actions:
                        kwargs = ", ".join(f"{k}={v}" for k, v in action.kwargs.values())
                        lines.append(
                            f"        [File Action] {action.label} -> {action.module}.{action.callable}({kwargs})"
                        )

        return "\n".join(lines)
