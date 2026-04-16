import logging
import sys
import time
from threading import Thread
from typing import Callable, List

from windows_toasts import (
    InteractableWindowsToaster,
    Toast,
    ToastActivatedEventArgs,
    ToastButton,
    ToastInputTextBox,
    WindowsToaster,
)

from bluepepper.core import init_logging


def handle_event(handler: List[dict], args: ToastActivatedEventArgs) -> None:
    """
    Returns a dictionary with two entries:
    - arguments: value of the button clicked to activate the Toast
    - inputs : values of the various inputs (text, combobox...)
    """
    result = args.__dict__ if isinstance(args, ToastActivatedEventArgs) else {}
    handler.append(result)


def show_toast_with_callback(
    toast: Toast,
    callback: Callable,
    dismissed_callback: Callable,
    toaster_name: str = "",
) -> None:

    # Create Toaster from the appropriate toaster class
    if toast.inputs or toast.actions:
        toaster = InteractableWindowsToaster(toaster_name)
    else:
        toaster = WindowsToaster(toaster_name)

    # Store toast events in a mutable object, so their change can be tracked in the while loop
    activated_handler = []
    dismissed_handler = []
    failed_handler = []
    toast.on_activated = lambda args: handle_event(activated_handler, args)
    toast.on_dismissed = lambda args: handle_event(dismissed_handler, args)
    toast.on_failed = lambda args: handle_event(failed_handler, args)

    # Show toast and wait for user response
    toaster.show_toast(toast)
    while True:
        time.sleep(1)
        if dismissed_handler:
            logging.info("Toast was dismissed")
            dismissed_handler.clear()
            if dismissed_callback:
                dismissed_callback()
            # Terminate thread
            sys.exit(0)

        if failed_handler:
            failed_handler.clear()
            logging.warning("Toast has failed")
            sys.exit(0)

        if activated_handler:
            if isinstance(toaster, InteractableWindowsToaster):
                interactable_toast_activated(
                    activated_handler, callback, dismissed_callback
                )
            else:
                non_interactable_toast_activated(activated_handler, callback)


def non_interactable_toast_activated(
    activated_handler: List[dict], callback: Callable
) -> None:
    # Clear handler to prevent callback being called multiple times
    # It may happen if the Toast logic is part of a loop
    activated_handler.clear()

    # Run callback and terminate thread
    callback()
    sys.exit(0)


def interactable_toast_activated(
    activated_handler: List[dict], callback: Callable, dismissed_callback: Callable
) -> None:
    button_result = activated_handler[0]["arguments"]
    kwargs = activated_handler[0]["inputs"]
    # Clear handler to prevent callback being called multiple times
    # It may happen if the Toast logic is part of a loop
    activated_handler.clear()

    if button_result == "cancel":
        logging.info("Toast cancelled by the user")
        if dismissed_callback:
            dismissed_callback()
        # Terminate thread
        sys.exit(0)

    # Run callback and terminate thread
    callback(**kwargs)
    sys.exit(0)


def start_toast_with_callback_thread(
    toast: Toast,
    callback: Callable,
    dismissed_callback: Callable | None = None,
    toaster_name: str = "",
):
    kwargs = {
        "toast": toast,
        "callback": callback,
        "dismissed_callback": dismissed_callback,
        "toaster_name": toaster_name,
    }
    thread = Thread(target=show_toast_with_callback, kwargs=kwargs, daemon=True)
    thread.start()


def print_stuff():
    print("Callback : Activated")


def print_hello(name: str):
    print(f"Callback : Hello {name}")


def print_dismissed():
    print("Callback : Dismissed")


if __name__ == "__main__":
    init_logging("toast")

    # Example of non-interactive toast
    toaster = WindowsToaster("PrintStuff")
    toast = Toast(["Click to print stuff"])
    start_toast_with_callback_thread(toast, print_stuff, print_dismissed)
    time.sleep(
        1
    )  # Wait a second to prevent windows displaying toasts in the wrong order

    # Example of interactive toast
    toast = Toast(["Please enter your details"])
    toast.AddInput(ToastInputTextBox("name", "Your name", "Barack Obama"))
    toast.AddAction((ToastButton("Submit", "ok")))
    toast.AddAction((ToastButton("Cancel", "cancel")))
    start_toast_with_callback_thread(toast, print_hello, print_dismissed)

    # An event loop is kept active to wait for the toast result
    while True:
        print("Event loop")
        time.sleep(1)
