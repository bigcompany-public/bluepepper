from __future__ import annotations

from typing import TYPE_CHECKING

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from bluepepper.core import database
from bluepepper.tools.browser.browser_config import Entity
from bluepepper.tools.browser.table_documents import TableDocuments
from bluepepper.tools.browser.table_files import TableFiles
from bluepepper.tools.browser.table_kinds import TableFileKinds
from bluepepper.tools.browser.table_tasks import TableTasks
from bluepepper.tools.tags.tag_filter_widget import TagFilterWidget

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_widget import BrowserWidget


class EntityTab(QWidget):
    """
    Create a new tab for an entity with filters and result tables.

    Args:
        self.entity.name: Internal name of the entity (e.g., 'asset', 'shot')
        entity_label: Display label for the entity (e.g., 'Assets', 'Shots')

    Returns:
        Dictionary containing references to all created widgets in this tab
    """

    def __init__(self, browser: BrowserWidget, entity: Entity) -> None:
        self.browser = browser
        self.entity = entity
        self.document_table: TableDocuments = None
        self.task_table: TableTasks = None
        self.kind_table: TableFileKinds = None
        self.file_table: TableFiles = None
        self.search_bar: SearchBar = None
        self.filter_comboboxes: list[FilterComboBox] = []
        super().__init__(browser)
        self.setup_ui()
        self.add_search_bar()
        self.add_document_table()
        self.add_task_table()
        self.add_kind_table()
        self.add_file_table()
        self.add_filter_widgets()
        self.setup_initial_state()
        self.setup_signals()

    def setup_ui(self) -> None:
        self.setObjectName(f"tab_{self.entity.name}")

        # Main layout for the tab
        self.tab_layout = QVBoxLayout(self)
        self.tab_layout.setContentsMargins(3, 3, 3, 3)

        # Frame for filters
        self.frame_filters_and_tags = QFrame(self)
        self.frame_filters_and_tags.setObjectName(f"frame_filters_{self.entity.name}")
        self.frame_filters_and_tags.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # self.frame_filters_and_tags.setProperty("depth", "0")
        self.layout_filters_and_tags = QVBoxLayout(self.frame_filters_and_tags)
        self.tab_layout.addWidget(self.frame_filters_and_tags)

        # Add frame for filters
        self.frame_filters = QFrame(self.frame_filters_and_tags)
        self.layout_filters = QHBoxLayout(self.frame_filters)
        self.label_filters = QLabel("Filters", self.frame_filters)
        self.label_filters.setMinimumWidth(60)
        self.layout_filters.setContentsMargins(3, 3, 3, 3)
        self.label_filters.setProperty("tag", "H2")
        self.layout_filters.addWidget(self.label_filters)
        self.layout_filters_and_tags.addWidget(self.frame_filters)

        # Add frame for tags
        self.frame_tags = QFrame(self.frame_filters_and_tags)
        self.layout_tags = QHBoxLayout(self.frame_tags)
        self.label_tags = QLabel("Tags", self.frame_tags)
        self.label_tags.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.label_tags.setMinimumWidth(60)
        self.layout_tags.setContentsMargins(3, 3, 3, 3)
        self.label_tags.setProperty("tag", "H2")
        self.layout_tags.addWidget(self.label_tags, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout_filters_and_tags.addWidget(self.frame_tags)
        self.tag_filter_widget = TagFilterWidget(tag_collection=self.entity.collection)
        self.tag_filter_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Adjust tag filter height
        num_tags = len(self.tag_filter_widget.get_tag_documents())
        if num_tags < 5:
            height = 35
        elif num_tags < 10:
            height = 62
        else:
            height = 90
        self.tag_filter_widget.setFixedHeight(height)
        self.layout_tags.addWidget(self.tag_filter_widget)

        # Add frame for other miscellaneous buttons
        self.frame_misc = QFrame(self)
        self.layout_misc = QHBoxLayout(self.frame_misc)
        self.layout_misc.setContentsMargins(0, 0, 0, 0)
        spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_misc.addItem(spacer)
        self.pause_update_checkbox = QCheckBox("Pause File Update")
        self.layout_misc.addWidget(self.pause_update_checkbox)
        self.update_files_button = QPushButton("Update")
        self.update_files_button.setProperty("status", "important")
        self.layout_misc.addWidget(self.update_files_button)
        self.tab_layout.addWidget(self.frame_misc)

        # Frame for results tables
        self.frame_results = QFrame(self)
        self.frame_results.setObjectName(f"frame_results_{self.entity.name}")
        self.frame_results.setProperty("depth", "0")
        self.frame_results.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_results = QHBoxLayout(self.frame_results)
        self.layout_results.setContentsMargins(3, 3, 3, 3)
        self.tab_layout.addWidget(self.frame_results)

    def add_search_bar(self) -> None:
        label = QLabel(self)
        label.setText("Search")
        self.layout_filters.addWidget(label)

        self.search_bar = SearchBar(self)
        self.layout_filters.addWidget(self.search_bar)

    def add_filter_widgets(self) -> None:
        for filter in self.entity.filters:
            label = QLabel(filter, self.frame_filters)
            self.layout_filters.addWidget(label)
            combobox = FilterComboBox(self, filter)
            self.layout_filters.addWidget(combobox)
            self.filter_comboboxes.append(combobox)

        spacer = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Minimum)
        self.layout_filters.addItem(spacer)

    def add_document_table(self):
        self.document_table = TableDocuments(self)
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(6)
        self.document_table.setSizePolicy(size_policy)
        self.layout_results.addWidget(self.document_table)

    def add_task_table(self):
        self.task_table = TableTasks(self)
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(5)
        self.task_table.setSizePolicy(size_policy)
        self.layout_results.addWidget(self.task_table)

    def add_kind_table(self):
        self.kind_table = TableFileKinds(self)
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(5)
        self.kind_table.setSizePolicy(size_policy)
        self.layout_results.addWidget(self.kind_table)

    def add_file_table(self):
        self.file_table = TableFiles(self)
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(10)
        self.file_table.setSizePolicy(size_policy)
        self.layout_results.addWidget(self.file_table)

    def setup_initial_state(self):
        # Updating the first filter combobox triggers the update of all following comboboxes
        # The last combobox itself triggers the update of documents
        self.filter_comboboxes[0].update_items()
        self.task_table.update_items()
        self.kind_table.update_items()

    def setup_signals(self):
        self.update_files_button.clicked.connect(self.update_files_clicked)
        self.tag_filter_widget.list_widget.itemSelectionChanged.connect(self.document_table.update_items)

    def update_files_clicked(self):
        self.file_table.update_items(force=True)

    @property
    def selected_tags(self) -> list[str]:
        return self.tag_filter_widget.selected_tags


class FilterComboBox(QComboBox):
    def __init__(self, tab: EntityTab, filter: str) -> None:
        super().__init__(tab)
        self.tab = tab
        self.collection = database.db.get_collection(tab.entity.collection)
        self.filter = filter
        self.setMinimumWidth(100)
        self.currentIndexChanged.connect(self.index_changed)

    def update_items(self):
        # Get only values that are possible, given the previous fields
        query = self.get_previous_fields_query()
        result = list(self.collection.find(query)) or []
        items = list(set([item.get(self.filter, "") for item in result]))
        items = sorted(items, key=str.lower)
        items = [item for item in items if item.strip()]  # remove if field is empty
        items.insert(0, "*")

        # Set new items
        self.clear()
        self.addItems(items)

    def get_next_combobox(self) -> FilterComboBox | None:
        """Returns the next filter combobox"""
        index = self.tab.filter_comboboxes.index(self)
        # Return None if this filter combobox is the last
        if index == len(self.tab.filter_comboboxes) - 1:
            return
        return self.tab.filter_comboboxes[index + 1]

    def get_previous_fields_query(self) -> dict[str, str]:
        """
        Returns a query generated with the fields that come before this one
        these query shall be used to get the available values for this field
        """
        index = self.tab.filter_comboboxes.index(self)
        if index == 0:
            return {}
        previous_comboboxes = self.tab.filter_comboboxes[:index]
        query = {
            filter_combobox.filter: filter_combobox.currentText()
            for filter_combobox in previous_comboboxes
            if not filter_combobox.currentText() == "*"
        }
        return query

    def update_next_combobox(self) -> None:
        """Updates the next combobox if there is one"""
        next_combobox = self.get_next_combobox()
        if not next_combobox:
            return
        next_combobox.update_items()

    def index_changed(self):
        """This method is triggered when the index of the combobox is changed"""
        self.update_next_combobox()
        # Only updates the documents if this is the last filter (or else, the
        # documents will be updated several times)
        if not self.get_next_combobox():
            # Ensure this is not triggered by the clear() method
            if self.currentIndex() != -1:
                self.tab.document_table.update_items()


class SearchBar(QLineEdit):
    def __init__(self, tab: EntityTab):
        super().__init__(tab)
        self.tab = tab
        self.setMinimumWidth(100)
        self.setMaximumWidth(150)
        tooltip = (
            "The search is not case-sensitive.",
            'You may make multiple search by using ";" between names',
            'For advanced search, you can write a mongodb query, for instance : {"type": "chr"}',
        )
        self.setToolTip("\n".join(tooltip))
        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        if not self.tab.document_table:
            return
        self.tab.document_table.update_items()
