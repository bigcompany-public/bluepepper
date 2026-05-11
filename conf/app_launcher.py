from __future__ import annotations

from dataclasses import dataclass, field


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
    kwargs: dict[str, str] = field(default_factory=dict[str, str])
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
        LauncherItem(
            label="Powershell",
            icon="software_powershell.png",
            module="bluepepper.softwares.powershell_launcher",
            function="open",
            tooltip="Opens Powershell with BluePepper venv activated",
        ),
    ]

    tools: list[LauncherItem] = [
        LauncherItem(
            label="Asset Tag Manager",
            icon="tag.png",
            module="bluepepper.tools.tags.tag_manager_widget",
            function="show_tag_manager_dialog",
            tooltip="Manage asset tags",
            kwargs={"tag_collection": "assets"},
        ),
        LauncherItem(
            label="Shot Tag Manager",
            icon="tag.png",
            module="bluepepper.tools.tags.tag_manager_widget",
            function="show_tag_manager_dialog",
            tooltip="Manage shot tags",
            kwargs={"tag_collection": "shots"},
        ),
    ]
