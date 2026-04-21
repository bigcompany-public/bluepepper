from __future__ import annotations

import importlib
import logging
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import qtawesome
from lucent import (
    Convention,
    LucentFileNotFoundError,
    LucentInconsistentFieldsError,
    LucentParseError,
)
from qtpy.QtCore import QEvent, QObject, Qt, Signal
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QAbstractItemView,
    QMenu,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
)
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from bluepepper.core import database
from bluepepper.gui.utils import get_icon
from bluepepper.tools.browser.browser_config import FileKind

# Imports used only for type checking : these will not be imported at runtime
if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_config import Entity, MenuAction
    from bluepepper.tools.browser.browser_tab import EntityTab
    from bluepepper.tools.browser.browser_widget import BrowserWidget


class FileWatcherHandler(FileSystemEventHandler, QObject):
    """Handler for file system events that emits Qt signals"""

    file_created = Signal(Path, dict)
    file_deleted = Signal(Path, dict)

    def __init__(
        self,
        convention: Convention,
        document: dict[str, str],
    ):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self)
        self.convention = convention
        self.document = document

    def _matches_convention(self, path: Path) -> bool:
        """Check if the path matches any of the watched documents' conventions"""
        # First check if the path matches the convention
        try:
            fields = self.convention.parse(path)
        except (
            LucentParseError,
            LucentInconsistentFieldsError,
        ):
            return False

        # If so, check if the extracted fields match the selected documents
        relevant_keys = [key for key in fields.keys() if key in self.document]
        perfect_match = all((self.document[key] == fields[key] for key in relevant_keys))
        if perfect_match:
            return True
        return False

    def on_created(self, event: FileSystemEvent):
        path = Path(event.src_path)
        if self._matches_convention(path):
            logging.debug(f"File created: {path}")
            self.file_created.emit(path, self.document)

    def on_deleted(self, event: FileSystemEvent):
        path = Path(event.src_path)
        logging.debug(f"File deleted: {path}")
        if self._matches_convention(path):
            self.file_deleted.emit(path, self.document)

    def on_moved(self, event: FileSystemEvent):
        src_path = Path(event.src_path)
        dst_path = Path(event.dest_path)
        logging.debug(f"File moved: {src_path} -> {dst_path}")
        if self._matches_convention(src_path):
            self.file_deleted.emit(src_path)
        if self._matches_convention(dst_path):
            self.file_created.emit(dst_path)


class TableFiles(QTableWidget):
    """
    This class adds signals to the provided table widget
    This method was chosen over inheriting from QTableWidget and initializing a
    new widget to keep as much control as possible in QtDesigner
    """

    def __init__(self, tab: EntityTab):
        self.tab = tab
        self.browser: BrowserWidget = tab.browser
        self.entity: Entity = tab.entity
        self.collection = database.db.get_collection(self.entity.collection)
        self.document_table = self.tab.document_table
        self.kind_table = self.tab.kind_table
        self.file_items = []
        self.observers: list[Observer] = []
        self.handlers: list[FileWatcherHandler] = []
        super().__init__(tab)
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        self.setColumnCount(1)
        size_policy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )
        self.setSizePolicy(size_policy)
        item = QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        self.setHorizontalHeaderLabels(["Files"])
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setHighlightSections(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setStretchLastSection(False)
        self.setSortingEnabled(True)

    def setup_signals(self):
        """Sets ut the signals of the table widget"""
        self.itemSelectionChanged.connect(self.file_changed)

    def file_changed(self):
        """This method is triggered when the file's selection has changed"""
        file_names = [item.path for item in self.get_selected_items()]
        logging.info(f"File selection changed to {file_names}")

    def get_selected_items(
        self,
    ) -> list[FileItem]:
        return self.selectedItems()

    def get_paths(
        self,
    ) -> list[tuple[Path, dict]]:
        kind = self.tab.kind_table.get_selected_kind()
        documents = self.tab.document_table.selected_documents
        if not kind or not documents:
            return []

        paths = self.search_existing_paths(
            kind.convention,
            documents,
        )
        return paths

    def search_existing_paths(
        self,
        convention: Convention,
        documents: list[dict[str, str]],
    ) -> list[tuple[Path, dict]]:
        if not documents:
            return []

        if len(documents) == 1:
            # return all files matching the pattern
            doc = documents[0]
            paths = convention.get_paths(doc)
            return [(path, doc) for path in paths]

        # return last path for each selected document
        paths = []
        for doc in documents:
            try:
                path = convention.get_last_path(doc)
                paths.append((path, doc))
            except LucentFileNotFoundError:
                pass
        return paths

    def update_items(self):
        self.clear_items()
        self.kill_watchdog_observers()
        self.add_file_items()
        self.start_watchdog_observers()

    def add_file_items(self):
        path_tuples = self.get_paths()
        for path_tuple in path_tuples:
            path, doc = path_tuple
            self.file_items.append(FileItem(doc, path))
        if not self.file_items:
            self.file_items = [FileItem(None)]

        # Add items to the table
        for item in self.file_items:
            row_number = self.rowCount()
            self.insertRow(row_number)
            self.setItem(row_number, 0, item)

    def clear_items(self):
        self.clearContents()
        self.setRowCount(0)
        self.file_items = []

    @property
    def selected_paths(
        self,
    ) -> list[Path]:
        items = self.selectedItems() or []
        items = [item for item in items if isinstance(item, FileItem)]
        paths = [item.path for item in items]
        return paths

    @property
    def selected_items(
        self,
    ) -> list[FileItem]:
        items = self.selectedItems() or []
        items = [item for item in items if isinstance(item, FileItem)]
        return items

    def kill_watchdog_observers(self):
        """Kill all observers and the corresponding handlers"""
        for observer in self.observers:
            observer.stop()
            observer.join(timeout=1.0)

        # Disconnect signals from handlers
        for handler in self.handlers:
            try:
                handler.file_created.disconnect()
                handler.file_deleted.disconnect()
            except (
                TypeError,
                RuntimeError,
            ):
                pass  # Signal already disconnected

        self.observers.clear()
        self.handlers.clear()
        logging.info("All watchdog observers stopped")

    def start_watchdog_observers(self):
        """
        For each selected document:
        - setup an observer looking for new files or deleted/moved files
        - setup a handler that adds and remove FileItems in the tableWidget
        - while the observers and handlers are running, the pyside app must stay responsive and avoid freezes
        """
        watch_dirs = self.get_dirs_to_watch()

        # Create handler and observers for each unique directory
        kind = self.tab.kind_table.get_selected_kind()
        for watch_dir, document in watch_dirs:
            # Create folder so a handler can be connected to it
            watch_dir.mkdir(
                exist_ok=True,
                parents=True,
            )

            # Create handler and connect its signals to slots
            handler = FileWatcherHandler(
                kind.convention,
                document,
            )
            handler.file_created.connect(self._on_file_created)
            handler.file_deleted.connect(self._on_file_deleted)

            observer = Observer()
            observer.schedule(
                handler,
                str(watch_dir),
                recursive=True,
            )
            observer.start()

            self.handlers.append(handler)
            self.observers.append(observer)

            logging.info(f"Started watching directory: {watch_dir}")

    def get_dirs_to_watch(
        self,
    ) -> list[tuple[Path, dict]]:
        kind = self.tab.kind_table.get_selected_kind()
        documents = self.tab.document_table.selected_documents
        if not kind or not documents:
            return []

        # A list is used instead of a set, becauses Path objects are not hashable
        unique_dirs_to_watch: list[Path] = []
        result = []
        for document in documents:
            _dir = self.get_dir_to_watch(
                kind.convention,
                document,
            )
            if _dir not in unique_dirs_to_watch:
                unique_dirs_to_watch.append(_dir)
                result.append((_dir, document))

        return sorted(result, key=lambda x: x[0])

    def get_dir_to_watch(
        self,
        convention: Convention,
        document: dict[str, str],
    ) -> Path:
        glob_pattern = convention.glob_pattern(document)
        parts = Path(glob_pattern).parts
        src_dir_parts: list[str] = []
        for part in parts:
            src_dir_parts.append(part)
            if "*" in part:
                break
        return Path(*src_dir_parts).parent

    def _on_file_created(self, path: Path, document: dict):
        """Slot called when a file is created - runs in main Qt thread"""
        # Check if file already exists in table
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if isinstance(item, FileItem) and item.path == path:
                return

        # Remove "No file found" item if it exists
        if self.rowCount() == 1:
            item = self.item(0, 0)
            if isinstance(item, FileItem) and item.path is None:
                self.removeRow(0)

        # Add new file item
        new_item = FileItem(document, path)
        row_number = self.rowCount()
        self.insertRow(row_number)
        self.setItem(row_number, 0, new_item)
        logging.info(f"Added file to table: {path}")

    def _on_file_deleted(self, path: Path, document: dict):
        """Slot called when a file is deleted - runs in main Qt thread"""
        # Find and remove the item
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if isinstance(item, FileItem) and item.path == path:
                self.removeRow(row)
                logging.info(f"Removed file from table: {path}")
                break

        # Add "No file found" if table is empty
        if self.rowCount() == 0:
            no_file_item = FileItem(None)
            self.insertRow(0)
            self.setItem(0, 0, no_file_item)

    @property
    def selected_kind(self) -> FileKind:
        return self.kind_table.selected_kind

    def contextMenuEvent(self, event: QEvent):
        """
        This method pops a Qmenu widget when the user right clicks on the table
        """
        if not self.entity.document_actions:
            return
        menu = TableFilesMenu(
            tab=self.tab,
            kind=self.selected_kind,
            event=event,
        )
        menu.exec_(event.globalPos())


class FileItem(QTableWidgetItem):
    """This class represents a file item within the TableFiles widget"""

    def __init__(
        self,
        document: Optional[dict] = None,
        path: Optional[Path] = None,
    ):
        self.document = document
        self.path = path
        super().__init__("")
        self.set_label()
        self.set_enabled()

    def set_label(self):
        self.setText(self.path.name if self.path else "No file found")

    def set_enabled(self):
        if not self.path:
            self.setFlags(self.flags() ^ Qt.ItemFlag.ItemIsEnabled)


class TableFilesMenu(QMenu):
    def __init__(
        self,
        tab: EntityTab,
        kind: FileKind,
        event: QEvent,
    ):
        super().__init__(tab)
        self.tab = tab
        self.kind = kind
        self._event = event
        self.entity = self.tab.entity
        self.register_actions()

    def register_actions(self):
        for action in self.get_actions_to_register():
            self.register_action(action)

    def get_actions_to_register(self):
        # Only register action if the selected documents respect the filter
        items = self.tab.file_table.selected_items
        if not items:
            return []

        filtered_actions = []
        for action in self.kind.file_actions:
            # If the action has no specific filter, just add it
            if not action.doc_filter and not action.path_filter:
                filtered_actions.append(action)
                continue

            at_least_one_item_matches_doc_filter = not bool(action.doc_filter)
            at_least_one_item_matches_path_filter = not bool(action.path_filter)

            for item in items:
                if action.doc_filter and not at_least_one_item_matches_doc_filter:
                    at_least_one_item_matches_doc_filter = action.doc_filter(item.document)

                if action.path_filter and not at_least_one_item_matches_path_filter:
                    at_least_one_item_matches_path_filter = action.path_filter(item.path)

            if at_least_one_item_matches_doc_filter and at_least_one_item_matches_path_filter:
                filtered_actions.append(action)

        return filtered_actions

    def register_action(self, menu_action: MenuAction):
        action = self.addAction(menu_action.label)

        # Set icon
        icon = None
        if menu_action.icon:
            icon = QIcon(get_icon(menu_action.icon).as_posix())
        elif menu_action.qta_icon:
            icon = qtawesome.icon(
                menu_action.qta_icon,
                scale_factor=1.1,
                color=menu_action.qta_icon_color,
            )

        if icon:
            action.setIcon(icon)

        # Import the module and get the callable
        module = importlib.import_module(menu_action.module)
        func = getattr(module, menu_action.callable)

        def execute_on_all_files():
            # Keep only items that match both document & path filters
            items = self.tab.file_table.selected_items
            if menu_action.doc_filter:
                items = [item for item in items if menu_action.doc_filter(item.document)]
            if menu_action.path_filter:
                items = [item for item in items if menu_action.path_filter(item.path)]

            # Conform kwargs
            kwargs = {}
            for (
                key,
                value,
            ) in menu_action.kwargs.items():
                kwargs[key] = value
                if value == "<documents>":
                    kwargs[key] = [item.document for item in items]
                elif value == "<document_names>":
                    kwargs[key] = [item.document[self.entity.name] for item in items]
                elif value == "<document_ids>":
                    kwargs[key] = [item.document["_id"] for item in items]
                elif value == "<browser>":
                    kwargs[key] = self.tab.browser
                elif value == "<convention>":
                    kwargs[key] = self.kind.convention
                elif value == "<paths>":
                    kwargs[key] = [item.path for item in items]

            # Execute callback with provided kwargs
            callback = partial(func, **kwargs)
            callback()

        # Create a wrapper that calls the function for each selected document
        def execute_on_each_file():
            # Keep only items that match both document & path filters
            items = self.tab.file_table.selected_items
            if menu_action.doc_filter:
                items = [item for item in items if menu_action.doc_filter(item.document)]
            if menu_action.path_filter:
                items = [item for item in items if menu_action.path_filter(item.path)]

            for item in items:
                document = item.document
                path = item.path
                # Format kwargs
                kwargs = {}
                for key, value in menu_action.kwargs.items():
                    kwargs[key] = value
                    if value == "<document>":
                        kwargs[key] = document
                    elif value == "<document_name>":
                        kwargs[key] = document[self.tab.entity.name]
                    elif value == "<document_id>":
                        kwargs[key] = document["_id"]
                    elif value == "<browser>":
                        kwargs[key] = self.tab.browser
                    elif value == "<convention>":
                        kwargs[key] = self.kind.convention
                    elif value == "<path>":
                        kwargs[key] = path

                # Execute callback with provided kwargs
                callback = partial(func, **kwargs)
                callback()

        # What happens on click depends on the kwargs
        # Depending on the situation, the function may need a list of documents, or run the function
        # for each document, or manipulate the browser altogether
        args = [
            "<document>",
            "<document_id>",
            "<document_name>",
            "<path>",
        ]
        if any([arg in args for arg in menu_action.kwargs.values()]):
            action.triggered.connect(execute_on_each_file)
            return

        action.triggered.connect(execute_on_all_files)
