from __future__ import annotations

import importlib
from functools import partial
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import qtawesome
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QMenu

from bluepepper.gui.utils import get_icon
from bluepepper.tools.browser.browser_config import MenuAction

if TYPE_CHECKING:
    from bluepepper.tools.browser.browser_tab import EntityTab


class BrowserMenu(QMenu):
    """Shared menu behavior for browser context menus."""

    PLACEHOLDER_HANDLERS = {
        "<browser>": "_resolve_browser",
        "<convention>": "_resolve_convention",
        "<documents>": "_resolve_documents",
        "<document_names>": "_resolve_document_names",
        "<document_ids>": "_resolve_document_ids",
        "<document>": "_resolve_document",
        "<document_name>": "_resolve_document_name",
        "<document_id>": "_resolve_document_id",
        "<paths>": "_resolve_paths",
        "<path>": "_resolve_path",
    }

    def __init__(
        self,
        tab: EntityTab,
        event,
        actions: list[MenuAction],
        targets: list[Any],
        kind=None,
    ):
        super().__init__(tab)
        self.tab = tab
        self._event = event
        self.kind = kind
        self.menu_actions = actions
        self.targets = targets
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
        func = getattr(module, menu_action.callable)

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
        if not self.targets:
            return []

        targets = []
        for target in self.targets:
            document = self._extract_document(target)
            path = self._extract_path(target)
            if menu_action.doc_filter and not menu_action.doc_filter(document):
                continue
            if menu_action.path_filter and not menu_action.path_filter(path):
                continue
            targets.append(target)

        return targets

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
        if isinstance(value, str) and value in self.PLACEHOLDER_HANDLERS:
            handler_name = self.PLACEHOLDER_HANDLERS[value]
            handler = getattr(self, handler_name)
            return handler(item=item, items=items)
        return value

    def _resolve_browser(self, item: Any = None, items: Optional[List[Any]] = None) -> Any:
        return self.tab.browser

    def _resolve_convention(self, item: Any = None, items: Optional[List[Any]] = None) -> Any:
        return self.kind.convention if self.kind else None

    def _resolve_documents(self, item: Any = None, items: Optional[List[Any]] = None) -> list[dict]:
        if items is None:
            return []

        documents: list[dict] = []
        for target in items:
            document = self._extract_document(target)
            if document is not None:
                documents.append(document)
        return documents

    def _resolve_document_names(self, item: Any = None, items: Optional[List[Any]] = None) -> list[str]:
        return [doc[self.entity.name] for doc in self._resolve_documents(item=item, items=items)]

    def _resolve_document_ids(self, item: Any = None, items: Optional[List[Any]] = None) -> list[str]:
        return [doc["_id"] for doc in self._resolve_documents(item=item, items=items)]

    def _resolve_document(self, item: Any = None, items: Optional[List[Any]] = None) -> Optional[dict]:
        if item is not None:
            return self._extract_document(item)
        if items:
            return self._extract_document(items[0])
        return None

    def _resolve_document_name(self, item: Any = None, items: Optional[List[Any]] = None) -> Optional[str]:
        document = self._resolve_document(item=item, items=items)
        return document[self.entity.name] if document else None

    def _resolve_document_id(self, item: Any = None, items: Optional[List[Any]] = None) -> Optional[str]:
        document = self._resolve_document(item=item, items=items)
        return document["_id"] if document else None

    def _resolve_paths(self, item: Any = None, items: Optional[List[Any]] = None) -> list[Any]:
        if items is None:
            return []
        return [self._extract_path(target) for target in items if self._extract_path(target) is not None]

    def _resolve_path(self, item: Any = None, items: Optional[List[Any]] = None) -> Any:
        if item is not None:
            return self._extract_path(item)
        if items:
            return self._extract_path(items[0])
        return None

    def _extract_document(self, target: Any) -> Optional[dict]:
        if isinstance(target, dict):
            return target
        return getattr(target, "document", None)

    @staticmethod
    def _extract_path(target: Any) -> Optional[Any]:
        if isinstance(target, dict):
            return None
        return getattr(target, "path", None)
