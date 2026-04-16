"""
This module contains the functions needed to easily execute callables from strings
"""

from importlib import import_module
from typing import Any


def run_callable(
    module: str,
    function: str = None,
    cls: str = None,
    args: list = None,
    kwargs: dict = None,
    method: str = None,
    static_method: str = None,
    method_args: list = None,
    method_kwargs: dict = None,
) -> Any:
    args = args or []
    kwargs = kwargs or {}
    method_args = method_args or []
    method_kwargs = method_kwargs or {}

    if function:
        return run_function(module=module, function=function, args=args, kwargs=kwargs)
    elif cls and not (method or static_method):
        return init_class(module=module, cls=cls, args=args, kwargs=kwargs)
    elif cls and method:
        return run_method(
            module=module,
            cls=cls,
            method=method,
            args=args,
            kwargs=kwargs,
            method_args=method_args,
            method_kwargs=method_kwargs,
        )
    elif cls and static_method:
        return run_static_method(
            module=module, cls=cls, static_method=static_method, method_args=method_args, method_kwargs=method_kwargs
        )


def run_function(module: str, function: str, args: list = None, kwargs: dict = None) -> Any:
    args = args or []
    kwargs = kwargs or {}
    module = import_module(module)
    function = getattr(module, function)
    return function(*args, **kwargs)


def init_class(module: str, cls: str, args: list = None, kwargs: dict = None) -> object:
    args = args or []
    kwargs = kwargs or {}
    module = import_module(module)
    cls = getattr(module, cls)
    return cls(*args, **kwargs)


def run_method(
    module: str,
    cls: str,
    method: str,
    args: list = None,
    kwargs: dict = None,
    method_args: list = None,
    method_kwargs: dict = None,
) -> object:
    args = args or []
    kwargs = kwargs or {}
    method_args = method_args or []
    method_kwargs = method_kwargs or {}
    module = import_module(module)
    cls = getattr(module, cls)
    cls = cls(*args, **kwargs)
    method = getattr(cls, method)
    return method(*method_args, **method_kwargs)


def run_static_method(
    module: str, cls: str, static_method: str, method_args: list = None, method_kwargs: dict = None
) -> object:
    method_args = method_args or []
    method_kwargs = method_kwargs or {}
    module = import_module(module)
    cls = getattr(module, cls)
    static_method = getattr(cls, static_method)
    return static_method(*method_args, **method_kwargs)
