"""
This module initializes BluePepper within blender. This actually covers :
- Initialization of the logging handler
- Declaration of the BluePepper Addon
- Register Operators
- Register Panels
- Add custom icons
- Set custom shortcuts
"""

import logging
from pathlib import Path

import bpy
import bpy.utils.previews  # Must be imported explicitely

from bluepepper.core import init_logging
from bluepepper.gui.utils import get_icon

bl_info = {
    "name": "BluePepper Addon",
    "author": "Tristan Languebien // Big Company",
    "version": (1, 0),
    "blender": (5, 1, 0),
    "category": "Development",
    "warning": "",
    "wiki_url": "",
}


#####################################
#               PANELS              #
#####################################


def get_preview_collections():
    """
    Creates a preview collection object that contains all the icons
    from the gui/icons directory. A preview collection is needed in order to use
    custom icons within panels. See the domentation for more insight :
    https://docs.blender.org/api/current/bpy.utils.previews.html
    """
    pcoll = bpy.utils.previews.new()
    icon_dir = Path(get_icon(""))
    icon_paths = icon_dir.iterdir()
    extensions = [".png"]
    for icon_path in icon_paths:
        if icon_path.suffix in extensions:
            name = icon_path.stem
            # Images must be added with a unique name
            pcoll.load(f"BIG_{name.upper()}_{icon_path.suffix[1:].upper()}", icon_path.as_posix(), "IMAGE")
    return pcoll


pcoll = get_preview_collections()
panel_scale_y = 1.3
panel_scale_x = 1.2


class BLUEPEPPER_PT_mainPanel(bpy.types.Panel):
    """Creates a Panel in the 3D_VIEW context"""

    bl_label = "BluePepper"
    bl_idname = "TOOLS_PT_bluepepper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BluePepper"

    def draw(self, context):
        layout = self.layout
        layout.scale_x = panel_scale_x
        layout.scale_y = panel_scale_y
        row = layout.row()
        row.label(text="This panel is empty")


class BLUEPEPPER_PT_devPanel(bpy.types.Panel):
    """Creates a subpanel inside the BLUEPEPPER_PT_mainPanel Panel"""

    bl_label = "Dev"
    bl_idname = "TOOLS_PT_bluepepperDev"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BluePepper"
    bl_parent_id = "TOOLS_PT_bluepepper"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.scale_x = panel_scale_x
        layout.scale_y = panel_scale_y
        row = layout.row()
        row.label(text="This panel is empty")


#####################################
#       REGISTER/UNREGISTER         #
#####################################

operator_classes = []
panel_classes = [
    BLUEPEPPER_PT_mainPanel,
    BLUEPEPPER_PT_devPanel,
]
addon_keymaps = []


def register():
    logging.info("Initializing BluePepper Addon")

    for op_class in operator_classes:
        logging.info(f"Registering operator {op_class.bl_idname}")
        bpy.utils.register_class(op_class)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

    # register panels
    for panel_class in panel_classes:
        logging.info(f"Registering panel {panel_class.bl_idname}")
        bpy.utils.register_class(panel_class)

    logging.info("Configuring bluepepper shortcuts")

    # Replace ctrl+shift+s shortcut so it uses BigSaveAs instead of regular save
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        pass


def unregister():
    for op_class in operator_classes:
        bpy.utils.unregister_class(op_class)

    # Unregister panels
    for panel_class in panel_classes:
        bpy.utils.unregister_class(panel_class)

    # Remove the custom shortcut
    wm = bpy.context.window_manager
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def menu_func(self, context):
    for op_class in operator_classes:
        self.layout.operator(op_class.bl_idname)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    init_logging("blender")
    register()
