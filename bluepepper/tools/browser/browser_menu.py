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

    PLACEHOLDERS = {
        "<browser>": lambda self, item=None, items=None, documents=None: self.tab.browser,
        "<convention>": lambda self, item=None, items=None, documents=None: getattr(self, "kind", None).convention if getattr(self, "kind", None) else None,
        "<documents>": lambda self, item=None, items=None, documents=None: self._resolve_documents(documents, items),
        "<document_names>": lambda self, item=None, items=None, documents=None: [doc[self.entity.name] for doc in self._resolve_documents(documents, items)],
        "<document_ids>": lambda self, item=None, items=None, documents=None: [doc["_id"] for doc in self._resolve_documents(documents, items)],
        "<document>": lambda self, item=None, items=None, documents=None: self._resolve_document(item, items),
        "<document_name>": lambda self, item=None, items=None, documents=None: self._extract_document(item, items)[self.entity.name],
        "<document_id>": lambda self, item=None, items=None, documents=None: self._extract_document(item, items)["_id"],
        "<paths>": lambda self, item=None, items=None, documents=None: [self._extract_path(item) for item in items or []],
        "<path>": lambda self, item=None, items=None, documents=None: self._extract_path(item, items),
    }

    def __init__(self, tab: EntityTab, event, kind=None):
        super().__init__(tab)
        self.tab = tab
        self._event = event
        self.kind = kind
        self.entity = self.tab.entity
        self.register_actions()

    def register_actions(self):
        for action in self.get_actions_to_register():
            self.register_action(action)

    def get_actions(self):
        raise NotImplementedError

    def get_action_targets(self, menu_action: MenuAction):
        raise NotImplementedError

    def get_actions_to_register(self):
        return [action for action in self.get_actions() if bool(self.get_action_targets(action))]

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
        mode = self.infer_mode(menu_action)
        if mode == "each":
            for target in targets:
                kwargs = self.resolve_kwargs(menu_action.kwargs, item=target, items=targets)
                callback = partial(func, **kwargs)
                callback()
            return

        kwargs = self.resolve_kwargs(menu_action.kwargs, items=targets)
        callback = partial(func, **kwargs)
        callback()

    def infer_mode(self, menu_action: MenuAction) -> str:
        if menu_action.mode != "auto":
            return menu_action.mode
        if any(keyword in menu_action.kwargs.values() for keyword in ("<document>", "<document_id>", "<document_name>", "<path>")):
            return "each"
        return "all"

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
        if isinstance(value, str) and value in self.PLACEHOLDERS:
            return self.PLACEHOLDERS[value](self, item=item, items=items)
        return value

    def _resolve_documents(self, documents: Optional[List[Any]], items: Optional[List[Any]]) -> List[dict]:
        if documents is not None:
            return documents
        if items is None:
            return []
        return [self._extract_document(item) for item in items if self._extract_document(item) is not None]

    def _resolve_document(self, item: Any, items: Optional[List[Any]]) -> Optional[dict]:
        if item is not None:
            return self._extract_document(item)
        if items:
            return self._extract_document(items[0])
        return None

    def _extract_document(self, item: Any, items: Optional[List[Any]] = None) -> dict:
        if item is None and items:
            item = items[0]
        if isinstance(item, dict):
            return item
        return getattr(item, "document", None)

    @staticmethod
    def _extract_path(item: Any, items: Optional[List[Any]] = None) -> Optional[Any]:
        if item is None and items:
            item = items[0]
        if item is None:
            return None
        return getattr(item, "path", None)
