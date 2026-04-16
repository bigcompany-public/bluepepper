from __future__ import annotations

import json
import sys
from contextlib import suppress
from dataclasses import dataclass
from typing import Callable, Dict, List

from lucent import Rule
from qtpy.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from bluepepper.asset_creator import AssetCreator
from bluepepper.core import codex, database
from bluepepper.database import Collection
from bluepepper.gui.utils import format_widgets, stylesheet
from bluepepper.gui.widgets.outcome_popups.outcome_popups import OutcomePopup
from bluepepper.shot_creator import ShotCreator


class FieldLabel(QLabel):
    def __init__(self, field: str, entity: str):
        super().__init__(field)
        self.setObjectName(f"label_{entity}_{field}")
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)


class FieldLineEdit(QLineEdit):
    def __init__(self, entity_tab: EntityTab, field: str):
        super().__init__()
        self.field = field
        self.entity_tab = entity_tab
        self.rule: Rule = codex.rules.get_rule_by_name(field)
        self.setObjectName(f"le_{self.entity_tab.entity}_{field}")
        self.setFixedWidth(150)
        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self) -> None:
        if self.is_valid:
            self.setProperty("status", "ok")
            self.setToolTip("")
        else:
            self.setProperty("status", "error")
            self.setToolTip(self.rule.get_mismatch_message(self.text()))
        self.setStyleSheet(stylesheet)

        self.entity_tab.toggle_create_button()

    @property
    def is_valid(self) -> bool:
        return self.rule.match(self.text())

    def reset(self):
        self.setText("")
        self.setProperty("status", "")
        self.setStyleSheet(stylesheet)


class FieldComboBox(QComboBox):
    def __init__(
        self, entity_tab: EntityTab, field: str, row_index: int, collection: Collection
    ):
        super().__init__()
        self.entity_tab = entity_tab
        self.entity = entity_tab.entity
        self.field = field
        self.row_index = row_index
        self.collection = collection
        self.setObjectName(f"cbb_{self.entity}_{field}")
        self.setFixedWidth(150)
        self.currentIndexChanged.connect(self._item_changed)

    def update_items(self) -> None:
        if self.isHidden():
            return

        # Get values + an extra "Custom" value
        values = self.get_possible_values()
        values.append("Custom")

        # Add items to the combobox
        self.blockSignals(True)
        self.clear()
        self.addItems(values)
        self.blockSignals(False)

        # Toggle other widgets
        self.toggle_line_edit_visibility()
        self.entity_tab.toggle_create_button()

    def get_possible_values(self) -> list[str]:
        # If the previous field is set to "Custom", all subsequent fields should be custom as well
        if self.row_index != 0:
            previous_combobox_value = self.entity_tab._rows[
                self.row_index - 1
            ].combobox.currentText()
            if previous_combobox_value == "Custom":
                return []

        # Otherwise, get all documents that match the previous fields
        query = self.entity_tab._previous_query(self.row_index)
        documents: List[dict[str, str]] = list(self.collection.find(query))
        values = {doc.get(self.field, "").strip() for doc in documents}
        values = sorted([value for value in values if value.strip()], key=str.lower)
        return values

    def _item_changed(self) -> None:
        # Update subsequent comboboxes
        for row in self.entity_tab._rows[self.row_index + 1 : -1]:
            row.combobox.update_items()

        # Toggle other widgets
        self.toggle_line_edit_visibility()
        self.entity_tab.toggle_create_button()

    def toggle_line_edit_visibility(self):
        row = self.entity_tab._rows[self.row_index]
        row.lineedit.setVisible(self.currentText() == "Custom")


@dataclass(slots=True)
class FieldRow:
    field: str
    label: FieldLabel
    combobox: FieldComboBox
    lineedit: FieldLineEdit

    @property
    def is_valid(self) -> bool:
        if self.combobox.isHidden() or self.combobox.currentText() == "Custom":
            return self.lineedit.is_valid
        return True


class EntityTab(QWidget):
    def __init__(
        self,
        parent: QWidget,
        entity: str,
        collection: Collection,
        required_fields: List[str],
        create_callback: Callable[[Dict[str, str]], None],
    ):
        super().__init__(parent)
        self.entity = entity
        self.collection = collection
        self.required_fields = required_fields
        self.collection = collection
        self.create_callback = create_callback

        self._rows: List[FieldRow] = []

        self.setup_ui()
        self.setup_initial_state()

    def setup_ui(self) -> None:
        # Make sure the widget is as small as it can be
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        main_layout = QVBoxLayout(self)
        main_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        # Add fields
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)

        for row_index, field in enumerate(self.required_fields):
            label = FieldLabel(field=field, entity=self.entity)
            grid_layout.addWidget(label, row_index, 0)

            combobox = FieldComboBox(
                entity_tab=self,
                field=field,
                row_index=row_index,
                collection=self.collection,
            )
            grid_layout.addWidget(combobox, row_index, 1)
            if field == self.entity:
                combobox.setHidden(True)

            lineedit = FieldLineEdit(entity_tab=self, field=field)
            column_index = 1 if field == self.entity else 2
            grid_layout.addWidget(lineedit, row_index, column_index)

            self._rows.append(FieldRow(field, label, combobox, lineedit))

        # Add create button
        self._create_button = QPushButton("Create")
        self._create_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._create_button.clicked.connect(self._on_create_clicked)
        self._create_button.setProperty("status", "important")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self._create_button)

        main_layout.addLayout(button_layout)

    def _update_create_button(self) -> None:
        for row in self._rows:
            if row.lineedit.isVisible() and not row.lineedit.is_valid:
                self._create_button.setEnabled(False)
                return
        self._create_button.setEnabled(True)

    def setup_initial_state(self) -> None:
        for row in self._rows:
            row.combobox.update_items()

    def _on_create_clicked(self) -> None:
        # Prevents the exception to be raised twice
        # (Since the app has an sys.excepthook setup that shows an error popup)
        with suppress(Exception):
            with OutcomePopup(show_success_popup=True, sound=True) as sp:
                fields = {}
                for row in self._rows:
                    key = row.field
                    if row.lineedit.isVisible():
                        value = row.lineedit.text()
                    else:
                        value = row.combobox.currentText()
                    fields[key] = value

                # Set success message
                sp.success_message = f"Successfully created {self.entity} with fields :\n{json.dumps(fields, indent=4)}"

                # Create entity
                self.create_callback(fields)

                # Reset lineedit
                self._rows[-1].lineedit.reset()

    def _previous_query(self, row: int) -> dict[str, str]:
        if row == 0:
            return {}

        query: dict[str, str] = {}
        for r in self._rows[:row]:
            if r.combobox.currentText() != "Custom":
                query[r.combobox.field] = r.combobox.currentText()

        query.pop(self.entity, None)
        return query

    def toggle_create_button(self):
        self._create_button.setEnabled(self.all_rows_are_valid)

    @property
    def all_rows_are_valid(self) -> bool:
        return all([row.is_valid for row in self._rows])


class EntityCreatorWidget(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._parent = parent
        self.attach_to_parent()
        self.init_ui()
        self.apply_stylesheet()

    def attach_to_parent(self) -> None:
        # Create layout if needed
        layout = self.get_layout()
        if not layout:
            layout = QVBoxLayout()
            self._parent.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.main_widget = QWidget(self)
        layout.addWidget(self.main_widget)

        self._parent.setWindowTitle("EntityCreator")
        self._parent.setObjectName("EntityCreator")

        self._parent.setMinimumSize(500, 250)

    def get_layout(self) -> QVBoxLayout:
        return self._parent.layout()  # type: ignore

    def init_ui(self) -> None:
        layout = QVBoxLayout(self.main_widget)
        tabs = QTabWidget(self.main_widget)
        layout.addWidget(tabs)

        asset_tab = EntityTab(
            parent=tabs,
            entity="asset",
            collection=database.assets,
            required_fields=codex.convs.asset_fields.required_fields,
            create_callback=create_asset,
        )
        tabs.addTab(asset_tab, "Asset")

        shot_tab = EntityTab(
            parent=tabs,
            entity="shot",
            collection=database.shots,
            required_fields=codex.convs.shot_fields.required_fields,
            create_callback=create_shot,
        )
        tabs.addTab(shot_tab, "Shot")

    def apply_stylesheet(self) -> None:
        self.main_widget.setStyleSheet(stylesheet)
        format_widgets(self.main_widget)


def create_asset(fields) -> None:
    AssetCreator(fields=fields).create()


def create_shot(fields) -> None:
    ShotCreator(fields=fields).create()


def main() -> None:
    app = QApplication(sys.argv)
    window = QWidget()
    ui = EntityCreatorWidget(window)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
