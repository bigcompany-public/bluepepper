from __future__ import annotations

import importlib
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

import qtawesome
from lucent import Convention
from qtpy.QtCore import QEvent
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QMenu

from bluepepper.gui.utils import get_icon
from bluepepper.tools.browser.browser_config import MenuAction

if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_widget import BrowserWidget


class BrowserMenu(QMenu):
    """Shared menu behavior for browser context menus."""

    @property
    def special_keywords_handlers(self) -> dict[str, Callable]:
        return {
            "<browser>": self._resolve_browser,
            "<convention>": self._resolve_convention,
            "<documents>": self._resolve_documents,
            "<document_names>": self._resolve_document_names,
            "<document_ids>": self._resolve_document_ids,
            "<document>": self._resolve_document,
            "<document_name>": self._resolve_document_name,
            "<document_id>": self._resolve_document_id,
            "<paths>": self._resolve_paths,
            "<path>": self._resolve_path,
        }

    def __init__(
        self,
        browser: BrowserWidget,
        event: QEvent,
        actions: list[MenuAction],
        target_type: str,
    ):
        super().__init__(browser.selected_tab)
        self.browser = browser
        self.target_type = target_type
        self.tab = browser.selected_tab
        self._event = event
        self.kind = self.tab.kind_table.selected_kind
        self.menu_actions = actions
        self.documents = self.tab.document_table.selected_documents
        self.path_items = self.tab.file_table.selected_items
        self.entity = self.tab.entity
        self.register_actions()

    def register_actions(self):
        for action in self.get_actions_to_register():
            self.register_action(action)

    def get_actions_to_register(self):
        return [action for action in self.menu_actions if bool(self.get_action_targets(action))]

    def get_action_icon(self, menu_action: MenuAction) -> Optional[QIcon]:
        if menu_action.icon:
            return QIcon(get_icon(menu_action.icon).as_posix())
        if menu_action.qta_icon:
            return qtawesome.icon(menu_action.qta_icon, scale_factor=1.1, color=menu_action.qta_icon_color)
        return None

    def register_action(self, menu_action: MenuAction):
        action = self.addAction(menu_action.label)
        icon = self.get_action_icon(menu_action)
        if icon:
            action.setIcon(icon)

        module = importlib.import_module(menu_action.module)
        func = getattr(module, menu_action.function)

        def execute_action(checked: bool = False, func=func, menu_action=menu_action):
            self.execute_menu_action(func, menu_action)

        action.triggered.connect(execute_action)

    def execute_menu_action(self, func: Any, menu_action: MenuAction):
        targets = self.get_action_targets(menu_action)
        if menu_action.mode not in {"each", "all"}:
            raise ValueError('MenuAction mode must be "each" or "all"')

        # Action on each selected
        if menu_action.mode == "each":
            for target in targets:
                kwargs = self.resolve_kwargs(menu_action.kwargs, item=target, items=targets)
                callback = partial(func, **kwargs)
                callback()
            return

        # Action on all selected
        kwargs = self.resolve_kwargs(menu_action.kwargs, items=targets)
        callback = partial(func, **kwargs)
        callback()

    def get_action_targets(self, menu_action: MenuAction):
        targets = []
        if self.target_type in ["document", "filekind"]:
            documents = self.documents
            for document in documents:
                if menu_action.doc_filter and not menu_action.doc_filter(document):
                    continue
                targets.append(document)
            return targets

        if self.target_type == "path":
            items = self.path_items
            for item in items:
                if menu_action.doc_filter and not menu_action.doc_filter(item.document):
                    continue
                if menu_action.path_filter and not menu_action.path_filter(item.path):
                    continue
                targets.append((item.path, item.document))
            return targets

        raise RuntimeError(f"Target type not supported - {self.target_type}")

    def resolve_kwargs(
        self,
        kwargs: Dict[str, Any],
        item: Any = None,
        items: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        resolved_kwargs: Dict[str, Any] = {}
        for key, value in kwargs.items():
            resolved_kwargs[key] = self.resolve_value(value, item=item, items=items)
        return resolved_kwargs

    def resolve_value(self, value: Any, item: Any = None, items: Optional[List[Any]] = None) -> Any:
        if isinstance(value, dict):
            return {key: self.resolve_value(sub_value, item=item, items=items) for key, sub_value in value.items()}
        if isinstance(value, list):
            return [self.resolve_value(sub_value, item=item, items=items) for sub_value in value]
        if isinstance(value, tuple):
            return tuple(self.resolve_value(sub_value, item=item, items=items) for sub_value in value)
        if isinstance(value, str) and value in self.special_keywords_handlers:
            handler = self.special_keywords_handlers[value]
            return handler(item=item, items=items)

        # Solve strings that contain a keyword
        if isinstance(value, str):
            for key in self.special_keywords_handlers.keys():
                if key in value:
                    handler = self.special_keywords_handlers[key]
                    result = handler(item=item, items=items)
                    return value.replace(key, str(result))

        return value

    def _resolve_browser(self, item=None, items=None) -> BrowserWidget:
        return self.tab.browser

    def _resolve_convention(self, item=None, items=None) -> Convention | None:
        if self.target_type in ["document", "task"]:
            return
        if not self.kind:
            return
        return self.kind.convention

    def _resolve_documents(self, items: list, item=None) -> list[dict]:
        if self.target_type == "path":
            items = [document for path, document in items]
        return items

    def _resolve_document_names(self, items: list, item=None) -> list[str]:
        if self.target_type == "path":
            items = [document for path, document in items]
        return [doc[self.entity.name] for doc in items]

    def _resolve_document_ids(self, items: list, item=None) -> list[str]:
        if self.target_type == "path":
            items = [document for path, document in items]
        return [doc["_id"] for doc in items]

    def _resolve_document(self, item: dict, items=None) -> dict:
        if self.target_type == "path":
            item = item[1]
        return item

    def _resolve_document_name(self, item: dict, items=None) -> str:
        if self.target_type == "path":
            item = item[1]
        return item[self.entity.name]

    def _resolve_document_id(self, item: dict, items=None) -> str:
        if self.target_type == "path":
            item = item[1]
        return item["_id"]

    def _resolve_paths(self, items: list[tuple[Path, dict]], item=None) -> list[str] | None:
        if self.target_type in ["document", "task", "filekind"]:
            return None
        return [item[0].as_posix() for item in items]

    def _resolve_path(self, item: tuple[Path, dict], items=None) -> str | None:
        if self.target_type in ["document", "task", "filekind"]:
            return None
        return item[0].as_posix()
