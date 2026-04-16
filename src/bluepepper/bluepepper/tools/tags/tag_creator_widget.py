from argparse import ArgumentParser

from lucent import Rule
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from bluepepper.core import codex
from bluepepper.gui.utils import get_qta_icon, stylesheet
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)
from bluepepper.gui.widgets.outcome_popups.outcome_popups import OutcomePopup
from bluepepper.tags import AssetTagCreator, ShotTagCreator, TagCreator
from bluepepper.tools.tags.tag_editor_widget import edit_asset_tag, edit_shot_tag


class CreateTagWidget(QWidget):
    # When "create" is pressed, emit a signal that returns the created document's id
    confirmed = Signal(str)

    def __init__(self, creator: TagCreator):
        super().__init__()
        self.creator = creator
        self.collection = creator.collection
        self.created_id: str = ""
        self.setup_ui()
        self.setup_signals()
        self.toggle_create_button()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        form_widget = QWidget()
        main_layout.addWidget(form_widget)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_widget.setLayout(form_layout)

        self.tag_label = QLabel("Tag Name:")
        self.le_name = QLineEdit()
        self.le_name.setMinimumWidth(200)
        self.le_name.setPlaceholderText("tagName")

        form_layout.setWidget(0, QFormLayout.LabelRole, self.tag_label)
        form_layout.setWidget(0, QFormLayout.FieldRole, self.le_name)

        self.create_button = QPushButton("Create")
        self.create_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.create_button.setProperty("status", "important")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.create_button)

        main_layout.addLayout(button_layout)

        self.create_button.clicked.connect(self.create_tag)

    def setup_signals(self):
        self.le_name.textChanged.connect(self.name_input_changed)

    def name_input_changed(self):
        if self.name_is_valid:
            self.le_name.setProperty("status", "ok")
            self.le_name.setToolTip("")
        else:
            self.le_name.setProperty("status", "error")
            self.le_name.setToolTip(self.rule.get_mismatch_message(self.le_name.text()))

        self.le_name.setStyleSheet(stylesheet)
        self.toggle_create_button()

    def toggle_create_button(self):
        self.create_button.setEnabled(self.name_is_valid)

    @property
    def rule(self) -> Rule:
        return codex.rules.tag

    @property
    def name_is_valid(self) -> bool:
        return self.rule.match(self.le_name.text())

    def create_tag(self):
        name = self.le_name.text().strip()
        if not name:
            return

        with OutcomePopup(show_success_popup=False, sound=True):
            self.creator.tag = name
            document = self.creator.create()

            self.created_id = document["_id"]
            self.confirmed.emit(document["_id"])


def create_asset_tag():
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-plus", scale_factor=1.25)
    widget = CreateTagWidget(creator=AssetTagCreator(tag=""))
    container = ContainerWidget(widget=widget, icon=icon, title="Create Tag")
    dialog = ContainerDialog(container)
    dialog.setMaximumSize(widget.sizeHint().width(), widget.sizeHint().height())
    widget.confirmed.connect(dialog.accept)
    if not dialog.exec():
        return

    edit_asset_tag(widget.created_id)


def create_shot_tag():
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-plus", scale_factor=1.25)
    widget = CreateTagWidget(creator=ShotTagCreator(tag=""))
    container = ContainerWidget(widget=widget, icon=icon, title="Create Tag")
    dialog = ContainerDialog(container)
    dialog.setMaximumSize(widget.sizeHint().width(), widget.sizeHint().height())
    widget.confirmed.connect(dialog.accept)
    if not dialog.exec():
        return

    edit_shot_tag(widget.created_id)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-a", "--asset", action="store_true")
    parser.add_argument("-s", "--shot", action="store_true")
    args = parser.parse_args()

    if args.asset:
        create_asset_tag()

    if args.shot:
        create_shot_tag()
