import json
import os
import sys
from pathlib import Path

import qtawesome
from bluepepper.core import root_dir
from qtpy import QtGui, QtWidgets
from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication


def get_qt_app():
    """Get Qt application.

    The function initializes new Qt application if it is not already
    initialized. It also sets some attributes to the application to
    ensure that it will work properly on high DPI displays.

    Returns:
        QtWidgets.QApplication: Current Qt application.
    """

    app = QApplication.instance()
    if app is None:
        for attr_name in (
            "AA_EnableHighDpiScaling",
            "AA_UseHighDpiPixmaps",
        ):
            attr = getattr(Qt, attr_name, None)
            if attr is not None:
                QApplication.setAttribute(attr)

        policy = os.getenv("QT_SCALE_FACTOR_ROUNDING_POLICY")
        if hasattr(QApplication, "setHighDpiScaleFactorRoundingPolicy") and not policy:
            QApplication.setHighDpiScaleFactorRoundingPolicy(
                Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
            )

        app = QApplication(sys.argv)

    return app


def get_qta_icon(
    name: str, scale_factor: float = 1.0, color: str | None = None
) -> QIcon:
    if not color:
        color = get_theme()["active"]
    return qtawesome.icon(name, scale_factor=scale_factor, color=color)


def get_icon(name: str) -> Path:
    icon_path = root_dir / f"bluepepper/gui/icons/{name}"
    if not icon_path.exists():
        raise FileNotFoundError(f"Icon not found : {icon_path}")
    return icon_path


def get_sound(name: str) -> Path:
    sound_path = root_dir / f"bluepepper/gui/sound/{name}"
    if not sound_path.exists():
        raise FileNotFoundError(f"Icon not found : {sound_path}")
    return sound_path


def get_theme(theme: str = "dark") -> dict[str, str]:
    path = root_dir / "bluepepper/gui/themes.json"
    with path.open("r") as json_file:
        theme_data = json.load(json_file)[theme]
    colors = translate_colors(theme, theme_data)
    return colors


def translate_colors(theme: str, theme_data: dict[str, str]) -> dict[str, str]:
    """
    This method converts color names into hex values
    """
    colors_file = root_dir / "bluepepper/gui/colors.json"
    with open(colors_file, "r", encoding="utf-8") as json_file:
        colors = json.loads(json_file.read())[theme]
    colors = {key: colors[value] for key, value in theme_data.items()}
    return colors


def format_widgets(widget: QtWidgets.QWidget):
    """
    Formats all the widgets and the widgets within it
    Warning : order is important, since some widgets are derived from others
    (in that regard, one can use a tighter operator than isinstance, such as
    if type(widget) == ...)
    """
    minimum_width = 130
    minimum_height = 25

    for child_widget in widget.children():
        # PushButton
        if isinstance(child_widget, QtWidgets.QPushButton):
            child_widget.setMinimumHeight(minimum_height)

        # Checkbox
        if isinstance(child_widget, QtWidgets.QCheckBox):
            child_widget.setMinimumHeight(minimum_height)

        # ComboBox
        elif isinstance(child_widget, QtWidgets.QComboBox):
            child_widget.setMinimumHeight(minimum_height)

        # Line Edit
        elif isinstance(child_widget, QtWidgets.QLineEdit):
            # Avoid lineedit being affected if it is within another widget
            if isinstance(widget, QtWidgets.QSpinBox):
                pass
            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                pass
            else:
                child_widget.setMinimumHeight(minimum_height)

        # Progress bar
        elif isinstance(child_widget, QtWidgets.QProgressBar):
            child_widget.setMinimumHeight(20)
            child_widget.setMinimumWidth(minimum_width)

        # QSpinBox
        elif isinstance(child_widget, QtWidgets.QSpinBox):
            child_widget.setMinimumHeight(minimum_height)
            child_widget.setMinimumWidth(70)

        elif isinstance(child_widget, QtWidgets.QDoubleSpinBox):
            child_widget.setMinimumHeight(minimum_height)
            child_widget.setMinimumWidth(70)

        # TreeView
        elif isinstance(child_widget, QtWidgets.QTreeView):
            root = child_widget.invisibleRootItem()
            items = []

            def recursively_get_items(parent_item):
                child_count = parent_item.childCount()
                for i in range(child_count):
                    item = parent_item.child(i)
                    items.append(item)
                    recursively_get_items(item)

            recursively_get_items(root)
            for item in items:
                # Get the data stored within the item
                # Data can be stored using : item.setData(0, 0, some_data)
                # import random
                # types = ["json", "python", "folder", "maya", "aftereffects"]
                # random_type = random.choice(types)
                # item.setData(100, 0, {"type": random_type})
                custom_data = item.data(100, 0)
                if not custom_data:
                    continue
                if custom_data.get("type") == "python":
                    item.setIcon(0, QtGui.QIcon(get_icon("icon_python.svg")))
                elif custom_data.get("type") == "folder":
                    item.setIcon(0, QtGui.QIcon(get_icon("icon_open.svg")))
                elif custom_data.get("type") == "maya":
                    item.setIcon(0, QtGui.QIcon(get_icon("software_maya.png")))
                elif custom_data.get("type") == "aftereffects":
                    item.setIcon(0, QtGui.QIcon(get_icon("software_aftereffects.png")))
                elif custom_data.get("type") == "json":
                    item.setIcon(0, QtGui.QIcon(get_icon("icon_json.svg")))
                elif custom_data.get("type") == "blend":
                    item.setIcon(0, QtGui.QIcon(get_icon("software_blender.png")))

        # QFrame
        elif isinstance(child_widget, QtWidgets.QFrame):
            child_widget.setFrameShape(QtWidgets.QFrame.NoFrame)

        format_widgets(child_widget)


def get_stylesheet(theme: str = "dark"):
    colors = get_theme(theme)
    stylesheet = f"""
    QMainWindow {{
        background-color:{colors["bg_two"]};
        color:{colors["text_color"]};
    }}
    QLabel[tag="H0"] {{
        color:{colors["H0_color"]};
        font-size:20px;
        font-weight:bold;
    }}
    QLabel[tag="H1"] {{
        color:{colors["H1_color"]};
        font-size:20px;
        font-weight:bold;
    }}

    QLabel[tag="H2"] {{
        color:{colors["H2_color"]};
        font-size:16px;
        font-weight:bold;
    }}

    QLabel[tag="H3"] {{
        color:{colors["H2_color"]};
        font-size:14px;
        font-weight:bold;
    }}

    QLabel[tag="H4"] {{
        color:{colors["H2_color"]};
        font-size:13px;
        font-weight:bold;
    }}

    QLabel[tag="H5"] {{
        color:{colors["H2_color"]};
        font-size:12px;
        font-weight:bold;
    }}

    QLabel[tag="H6"] {{
        color:{colors["H2_color"]};
        font-size:11px;
        font-weight:bold;
    }}

    QLabel[tag="droparea"] {{
        border-radius: 2px;
        border:1px solid {colors["active"]};
        font-size:11px;
        font-weight:bold;
    }}
    QLabel[tag="droparea"]::hover {{
        border:1px solid {colors["active"]};
        background-color: {colors["active"]};
        font-size:11px;
        font-weight:bold;
    }}

    QLabel {{
        color:{colors["text_color"]};
        font-size:12px;
        background-color:transparent;
    }}
    QLabel[status="important"] {{
        font-weight : bold;
    }}
    QLabel[status="error"] {{
        color:{colors["error"]};
        font-size:12px;
    }}
    QLabel[status="warning"] {{
        color:{colors["warning"]};
        font-size:12px;
    }}
    QLabel[status="ok"] {{
        color:{colors["ok"]};
        font-size:12px;
    }}
    QLabel[status="secondary"] {{
        color:{colors["text_color2"]};
        font-size:12px;
    }}
    QLabel[status="code"] {{
        border-radius: 2px;
        border:1px solid {colors["bg_three"]};
        color:{colors["text_color"]};
        font-size:12px;
        background-color:{colors["bg_two"]};
        padding: 5px;
    }}

    QCheckBox {{
        color:{colors["text_color"]};
        background-color:transparent;
    }}
    QCheckBox::indicator::hover {{border:1px solid {colors["active"]};}}
    QCheckBox::indicator {{
        width: 12px;
        height: 12px;
        border:1px solid {colors["outline"]};
        border-radius:3px;
        background-color:transparent;
    }}
    QCheckBox::indicator:checked {{
        border:1px solid {colors["active"]};
        background-color:{colors["active"]};
        image: url({get_icon("icon_check.svg").as_posix()});
    }}

    QFrame {{
        background-color:transparent;
    }}
    QFrame[tag="topbar"] {{
        background-color:{colors["bg_two"]};
    }}
    QFrame[tag="sidebar"] {{
        background-color:{colors["bg_two"]};
    }}
    QFrame[depth="0"] {{
        background-color:{colors["bg_three"]};
        border-radius:5px;
    }}

    QFrame[depth="1"] {{
        background-color:{colors["bg_one"]};
        border-radius:5px;
    }}

    QFrame[depth="2"] {{
        background-color:{colors["bg_three"]};
        border-radius:5px;
    }}
    QFrame[depth="3"] {{
        background-color:{colors["bg_three"]};
        border-radius:5px;
        border:1px solid {colors["outline"]};
    }}

    QComboBox {{
        border: 1px solid;
        border-color:{colors["text_color2"]};
        color:{colors["text_color"]};
        background-color:{colors["bg_one"]};
        border-radius:2px;
        padding-left:5px;
    }}
    QComboBox::hover {{
        border-color:{colors["button_hover"]};
    }}
    QComboBox QAbstractItemView {{
        outline: 0;
        border: none;
        background-color:{colors["bg_three"]};
    }}
    QComboBox QAbstractItemView::item {{
        color:{colors["text_color"]};
        height: 24px;
        padding-left: 5px;
    }}
    QComboBox QAbstractItemView::item::hover {{
        padding-left:5px;
    }}
    QComboBox QAbstractItemView::item:selected {{
        padding-left:5px;
        border-left: 2px solid {colors["active"]};
    }}
    QComboBox::separator {{
        background-color:{colors["outline"]};
    }}

    QLineEdit {{
        border: 1px solid;
        border-color:{colors["text_color2"]};
        border-radius:5px;
        padding-left:5px;
        color:{colors["text_color"]};
        background-color:{colors["bg_one"]};
    }}
    QLineEdit:hover {{
        border-color:{colors["active"]};
    }}
    QLineEdit:focus {{
        border-color:{colors["active"]};
    }}
    QLineEdit[status="error"] {{
        border: 1px solid;
        border-color:{colors["error"]};
    }}
    QLineEdit[status="ok"]::focus {{
        border: 1px solid;
        border-color:{colors["ok"]};
    }}
    QLineEdit:disabled {{
        border-color:{colors["disabled3"]};
        color:{colors["disabled3"]};
        background-color: rgba(255,255,255,5);
    }}
    QPushButton {{
        padding-left : 10px;
        padding-right : 10px;
        border: 1px solid;
        border-color:{colors["text_color2"]};
        color:{colors["text_color"]};
        border-radius:5px;
        background-color:transparent;
    }}
    QPushButton::hover {{
        border-color:{colors["button_hover"]};
    }}
    QPushButton::pressed {{
        background-color:{colors["button_pressed"]};
    }}
    QPushButton[status="ok"] {{
        border-color:{colors["ok"]};
    }}
    QPushButton[status="ok"]::hover {{
        border-color:{colors["button_hover"]};
    }}
    QPushButton[status="warning"] {{
        border-color:{colors["warning"]};
    }}
    QPushButton[status="warning"]::hover {{
        border-color:{colors["button_hover"]};
    }}
    QPushButton[status="error"] {{
        border-color:{colors["error"]};
    }}
    QPushButton[status="error"]::hover {{
        border-color:{colors["button_hover"]};
    }}
    QPushButton[status="important"] {{
        font-weight:bold;
        border: none;
        background-color:{colors["button_hover"]};
    }}
    QPushButton[status="icon_only"] {{
        qproperty-iconSize: 23px;
    }}
    QPushButton[status="icon_only_small"] {{
        qproperty-iconSize: 11px;
    }}
    QPushButton[status="important"]::hover {{
        border: 1px solid;
        border-color:{colors["text_color"]};
        background-color:{colors["button_hover"]};
    }}
    QPushButton[status="important"]::pressed {{
        border:none;
        background-color:{colors["button_pressed2"]};
    }}
    QPushButton[status="danger"] {{
        font-weight:bold;
        border:none;
        background-color:{colors["danger"]};
    }}
    QPushButton[status="danger"]::hover {{
        border: 1px solid;
        border-color:{colors["text_color"]};
        background-color:{colors["danger"]};
    }}
    QPushButton[status="danger"]::pressed {{
        border: 1px solid;
        border-color:{colors["danger"]};
        background-color:{colors["bg_one"]};
    }}
    QPushButton[visibility="transparent"] {{
        background-color:transparent;
        border: 0px;
    }}
    QPushButton[type="menuItem"] {{
        padding:0px;
        border-radius:0px;
        border-top-left-radius:2px;
        border-bottom-left-radius:2px;
        border: 0px solid;
        border-color:none;
        color:none;
    }}
    QPushButton[type="menuItem"]::hover {{
        border-radius:0px;
        border-top-left-radius:2px;
        border-bottom-left-radius:2px;
        border: 0px solid;
        border-color:none;
        border-left:2px solid {colors["text_color2"]};
        color:none;
    }}
    QPushButton[type="menuItem"]::focus {{
        border-radius:0px;
        border-top-left-radius:2px;
        border-bottom-left-radius:2px;
        border: 0px solid;
        border-color:none;
        border-left:2px solid {colors["active"]};
        background-color:{colors["bg_one"]};
        color:{colors["text_color"]};
    }}
    QPushButton:disabled {{
        border-color:{colors["disabled"]};
        background-color:{colors["disabled"]};
        color:{colors["disabled2"]};
    }}
    QPushButton[status="menu_bar_button"] {{
        border-radius:1px;
        background-color:transparent;
        border-color:transparent;
    }}
    QPushButton[status="menu_bar_button"]::hover {{
        border-radius:1px;
        background-color:{colors["disabled3"]};
        border-color:transparent;
    }}
    QPushButton[status="menu_bar_button_close"] {{
        border-radius:1px;
        background-color:transparent;
        border-color:transparent;
    }}
    QPushButton[status="menu_bar_button_close"]::hover {{
        border-radius:1px;
        background-color:{colors["error"]};
        border-color:transparent;
    }}

    QRadioButton {{
        color:{colors["text_color"]};
    }}

    QProgressBar {{
        border-radius:2px;
        background-color:{colors["bg_one"]};
        padding:3px;
        border-radius:10px;
        border:1px solid;
        border-color:{colors["outline"]};
        color:{colors["text_color"]};
        font-weight:bold;
        text-align: center;
    }}
    QProgressBar::chunk {{
        border-radius:5px;
        background:{colors["ok"]}
    }}
    QProgressBar[status="in_progress"]::chunk {{
        border-radius:5px;
        background:{colors["in_progress"]}
    }}
    QProgressBar[status="done"]::chunk {{
        border-radius:5px;
        background:{colors["done"]}
    }}
    QProgressBar[status="error"]::chunk {{
        border-radius:5px;
        background:{colors["error"]}
    }}
    QProgressBar[status="stuck"]::chunk {{
        border-radius:5px;
        background:{colors["stuck"]}
    }}
    QProgressBar[status="cancelled"]::chunk {{
        border-radius:5px;
        background:{colors["cancelled"]}
    }}

    QSpinBox {{
        border: 1px solid;
        background-color:{colors["bg_one"]};
        border-color:{colors["outline"]};
        color:{colors["text_color"]};
        padding-right: 15px;
        padding-left: 5px;
        border-radius:2px;
    }}
    SpinBox::up-button {{
        width:16;
        height:10;
        margin:1;
    }}
    SpinBox::down-button {{
        width:16;
        height:10;
        margin:1;
    }}
    QSpinBox::hover {{
        border-color:{colors["button_hover"]};
    }}
    QDoubleSpinBox {{
        border: 1px solid;
        background-color:{colors["bg_one"]};
        border-color:{colors["outline"]};
        color:{colors["text_color"]};
        padding-right: 15px;
        padding-left: 5px;
        border-radius:2px;
    }}
    QDoubleSpinBox::up-button {{
        width:16;
        height:10;
        margin:1;
    }}
    QDoubleSpinBox::down-button {{
        width:16;
        height:10;
        margin:1;
    }}
    QDoubleSpinBox::hover {{
        border-color:{colors["button_hover"]};
    }}

    QSlider::groove:horizontal {{
        height: 2px;
        background: {colors["text_color"]};
        border-radius:1px;
    }}
    QSlider::handle:horizontal {{
        background: {colors["button_hover"]};
        width: 16px;
        margin: -7px 0;
        border-radius:8px;
    }}
    QSlider::groove:vertical {{
        width: 2px;
        background: {colors["text_color"]};
        border-radius:1px;
    }}
    QSlider::handle:vertical {{
        background: {colors["button_hover"]};
        height: 16px;
        margin: 0 -7px;
        border-radius:8px;
    }}
    QSlider::handle::hover {{
        background-color:{colors["button_pressed2"]};
    }}

    QScrollBar:horizontal {{
        border: none;
        background: {colors["bg_two"]};
        height: 13px;
        margin: 0px 0px 0px 0px;
        border-radius: 0px;
    }}
    QScrollBar::handle:horizontal {{
        background: {colors["bg_four"]};
        margin:2px;
        min-width: 30px;
        border-radius: 4px
    }}
    QScrollBar::add-line:horizontal {{background: none;}}
    QScrollBar::sub-line:horizontal {{background: none;}}
    QScrollBar::up-arrow:horizontal {{background: none;}}
    QScrollBar::down-arrow:horizontal {{background: none;}}
    QScrollBar::add-page:horizontal {{background: none;}}
    QScrollBar::sub-page:horizontal {{background: none;}}

    QScrollBar:vertical {{
        border: none;
        background: {colors["bg_two"]};
        width: 13px;
        margin: 0px 0 0px 0;
        border-radius: 0px;
    }}
    QScrollBar::handle:vertical {{	
        background: {colors["bg_four"]};
        margin:2px;
        min-height: 30px;
        border-radius: 4px
    }}
    QScrollBar::add-line:vertical {{background: none;}}
    QScrollBar::sub-line:vertical {{background: none;}}
    QScrollBar::up-arrow:vertical {{background: none;}}
    QScrollBar::down-arrow:vertical {{background: none;}}
    QScrollBar::add-page:vertical {{background: none;}}
    QScrollBar::sub-page:vertical {{background: none;}}

    QScrollArea {{
        background-color:{colors["bg_three"]};
        border:1px solid;
        border-color:{colors["outline2"]};
        border-radius:2px;
    }}

    QTableWidget {{
        border:none;
        border-color: {colors["outline2"]};
        background-color: {colors["bg_one"]};
        padding: 2px;
        gridline-color: {colors["bg_three"]};
        color: {colors["text_color"]};
    }}
    QHeaderView {{background-color: transparent}}
    QHeaderView::section
    {{
        border:1px solid;
        border-color: {colors["bg_three"]};
        background-color: {colors["bg_two"]};
        color:{colors["text_color"]};
        padding: 3px;
    }}
    QHeaderView::section:checked::vertical
    {{
        border:1px solid;
        border-color: {colors["active"]};
        background-color: {colors["active"]};
        color:{colors["text_color"]};
        padding: 3px;
    }}
    QTableWidget QTableCornerButton::section {{
        background-color: {colors["bg_one"]};
        padding: 3px;
        border:1px solid;
        border-color: {colors["bg_three"]};
        border-top-left-radius: 3px;
    }}
    QTableView {{
        outline: 0;
    }}
    QTableView::item {{
        background-color: none;
    }}
    QTableView::item::selected {{
        background-color: {colors["active"]};
        color: {colors["bg_one"]};
    }}

    QTreeView {{
        border:1px solid;
        border-color: {colors["bg_three"]};
        border-radius:3px;
        background-color: {colors["bg_one"]};
        alternate-background-color: {colors["bg_two"]};
        padding: 2px;
        color: {colors["text_color"]};
    }}
    QTreeView::branch:has-children:closed {{
        image: url({get_icon("icon_arrow_right.svg").as_posix()});
        margin:5;
    }}
    QTreeView::branch:has-children:open {{
        image: url({get_icon("icon_arrow_down.svg").as_posix()});
        margin:5;
    }}

    QTabWidget::pane {{
        border: 1px solid {colors["outline"]};
        border-radius : 1px;
    }}
    QTabWidget::tab-bar {{left:0px;}}
    QTabBar::tab {{
        padding:5px;
        background-color:{colors["bg_two"]};
        color:{colors["text_color"]};
        border-left:1px solid {colors["outline2"]};
        border-right:1px solid {colors["outline2"]};
        border-top:1px solid {colors["outline2"]};
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 20ex;
    }}
    QTabBar::tab:selected {{
        margin-bottom: -2px;
        margin-left: -4px;
        margin-right: -4px;
        background-color:{colors["bg_three"]};
        border-left:1px solid {colors["active"]};
    }}
    QTabBar::tab:!selected {{
        margin-top: 2px;
    }}
    QTabBar::tab:first:selected {{margin-left: 0;}}
    QTabBar::tab:last:selected {{margin-right: 0;}}

    QTabBar QToolButton {{
        border: 1px solid {colors["active"]};
        border-radius: 3px;
        background-color: transparent;
    }}
    QTabBar QToolButton::disabled {{
        border: 1px solid transparent;
    }}

    QToolTip {{
        background-color: {colors["bg_four"]};
        color: {colors["text_color"]};
        border: 1px solid;
        border-color: {colors["text_color2"]};
        border-radius: 2px;
        border-left: 3px solid {colors["active"]};
        padding: 2px;
    }}

    QMenu {{
        background-color: {colors["bg_three"]};
        color: {colors["text_color"]};
        border: 1px solid;
        border-color: {colors["bg_four"]};
        border-radius: 1px;
        padding: 3px;
    }}
    QMenu::item:selected {{
        background-color: {colors["bg_four"]};   
    }}

    QListWidget {{
        border: 1px solid;
        border-color: {colors["bg_four"]};
        border-radius: 3px;
        background-color: {colors["bg_two"]};
        padding: 2px;
        color: {colors["text_color"]};
        outline: none;
    }}
    QListWidget::item {{
        border-radius: 3px;
        background-color: none;
    }}
    QListWidget::item::hover {{
        background-color: {colors["button_hover"]};
    }}

    .QWidget {{
        background-color:{colors["bg_one"]};
        color:{colors["text_color"]};
    }}
    .QWidget[visibility="transparent"] {{background-color:none}}
    """
    return stylesheet


stylesheet = get_stylesheet()

if __name__ == "__main__":
    print(get_stylesheet())
