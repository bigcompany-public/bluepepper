from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class LauncherItem:
    """Represents an external application to launch.

    Attributes:
        label: Display name for the launcher item.
        icon: Path to the icon file.
        module: Python module path for the launch function.
        function: Function name to call from the module.
        args: Command-line arguments to pass to the function.
        tooltip: Hover text describing the item.
    """

    label: str
    icon: str
    module: str
    function: str
    args: Sequence[str] = field(default_factory=list[str])
    tooltip: str = ""


@dataclass
class LauncherConfig:
    """Holds all apps and tools for the launcher.

    Attributes:
        apps: List of applications to launch.
        tools: List of tools to launch.
    """

    apps: list[LauncherItem] = field(default_factory=list[LauncherItem])
    tools: list[LauncherItem] = field(default_factory=list[LauncherItem])


class DefaultLauncherConfig(LauncherConfig):
    apps: list[LauncherItem] = [
        LauncherItem(
            label="Maya",
            icon="software_maya.png",
            module="bluepepper.softwares.maya.maya_launcher",
            function="open",
            tooltip="Opens Maya",
        ),
        LauncherItem(
            label="Blender",
            icon="software_blender.png",
            module="bluepepper.softwares.blender.blender_launcher",
            function="open",
            tooltip="Opens Blender",
        ),
    ]

    tools: list[LauncherItem] = [
        LauncherItem(
            label="Asset Tag Manager",
            icon="software_maya.png",
            module="bluepepper.tools.tags.tag_manager_widget",
            function="show_asset_tag_manager_dialog",
            tooltip="Manage asset tags",
        ),
        LauncherItem(
            label="Shot Tag Manager",
            icon="software_maya.png",
            module="bluepepper.tools.tags.tag_manager_widget",
            function="show_shot_tag_manager_dialog",
            tooltip="Manage shot tags",
        ),
    ]
