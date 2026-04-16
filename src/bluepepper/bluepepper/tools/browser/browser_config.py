"""
Application configuration module using dataclasses.

This module defines a hierarchical configuration structure for the BigBrowser application,
providing type-safe access to entities, workflows, tasks, and their associated actions.
"""

from dataclasses import dataclass, field
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
    kwargs: dict[str, str] = field(default_factory=dict[str, str])
    doc_filter: Callable = None
    path_filter: Callable = None


@dataclass
class Kind:
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
    kinds: dict[str, Kind] = field(default_factory=dict[str, Kind])
    doc_filter: Callable = None

    def __post_init__(self):
        if not self.label:
            self.label = self.name.capitalize()

    def add_kind(self, kind: Kind):
        if kind.name in self.kinds:
            raise RuntimeError(
                f'Cannot add kind with name "{kind.name}". Name is already used'
            )
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
            raise RuntimeError(
                f'Cannot add task with name "{task.name}". Name is already used'
            )
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
            raise RuntimeError(
                f'Cannot add entity with name "{entity.name}". Name is already used'
            )
        self.entities[entity.name] = entity

    def human_readable(self) -> str:
        lines: list[str] = []
        lines += [f'BigBrowser "{self.name}"', ""]

        for _, entity in self.entities.items():
            lines.append("[Entity] " + entity.label)
            for _, task in entity.tasks.items():
                lines.append("    [Task] " + task.label)
                for _, kind in task.kinds.items():
                    lines.append("      [Kind] " + kind.label)
                    for action in kind.kind_actions:
                        kwargs = ", ".join(
                            f"{k}={v}" for k, v in action.kwargs.values()
                        )
                        lines.append(
                            f"        [Kind Action] {action.label} -> {action.module}.{action.callable}({kwargs})"
                        )
                    for action in kind.file_actions:
                        kwargs = ", ".join(
                            f"{k}={v}" for k, v in action.kwargs.values()
                        )
                        lines.append(
                            f"        [File Action] {action.label} -> {action.module}.{action.callable}({kwargs})"
                        )

        return "\n".join(lines)
