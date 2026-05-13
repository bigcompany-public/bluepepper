"""
This module contains all functions susceptible to be called for bluepepper's main window
All of them have the BluePepperApp instance as first argument
"""

import logging
import os
import subprocess
import time
from pathlib import Path

from windows_toasts import Toast, ToastButton, WindowsToaster

from bluepepper.app.main_window.main_window import BluePepperApp
from bluepepper.toast import start_toast_with_callback_thread
from bluepepper.tools.batcher.job_model import JobData


def close(bluepepper_app: BluePepperApp):
    logging.info("Closing BluePepper App (FastAPI)")
    toast = Toast(["BluePepper will now close"])
    toast.AddAction((ToastButton("Not Now", "cancel")))
    toast.AddAction((ToastButton("Ok", "ok")))

    def callback():
        os._exit(0)

    def dismissed_callback():
        logging.info("BluePepper closing cancelled by the user")

    start_toast_with_callback_thread(toast, callback=callback, dismissed_callback=dismissed_callback)


def show(bluepepper_app: BluePepperApp):
    logging.info("Showing BluePepper App (FastAPI)")
    bluepepper_app.showNormal()


def minimize(bluepepper_app: BluePepperApp):
    logging.info("Minimizing BluePepper App (FastAPI)")
    bluepepper_app.showMinimized()


def maximize(bluepepper_app: BluePepperApp):
    logging.info("Maximizing BluePepper App (FastAPI)")
    bluepepper_app.showMaximized()


def log_info(bluepepper_app: BluePepperApp, message: str):
    logging.info(message)


def set_active_tab(bluepepper_app: BluePepperApp, index: int):
    bluepepper_app.page_buttons[index].click()


def update_browser_tags(bluepepper_app: BluePepperApp):
    if not bluepepper_app.browser:
        return
    for tab in bluepepper_app.browser.entity_tab_widgets:
        tab.tag_filter_widget.update_items()


def submit_batcher_job(
    bluepepper_app: BluePepperApp,
    name: str,
    description: str,
    script_path: str = "",
    script_args: list[str] | None = None,
    module: str = "",
    func: str = "",
    kwargs: dict | None = None,
    priority: int = 50,
    notify_when_done: bool = False,
    notify_message: str = "",
):
    if not bluepepper_app.batcher:
        return

    job_data = JobData(
        name=name,
        description=description,
        script_path=Path(script_path) if script_path else Path(),
        script_args=script_args or [],
        module=module,
        func=func,
        kwargs=kwargs or {},
        priority=priority,
        notify_when_done=notify_when_done,
        notify_message=notify_message,
    )
    bluepepper_app.batcher.add_job(job_data)


def show_toast(bluepepper_app: BluePepperApp, message: str):
    toaster = WindowsToaster("BluePepper")
    toast = Toast([message])
    toaster.show_toast(toast)


def reboot(bluepepper_app: BluePepperApp):
    logging.info("Rebooting computer (FastAPI)")

    toast = Toast(["BluePepper will now restart your computer"])
    toast.AddAction((ToastButton("Cancel Shutdown", "cancel")))
    toast.AddAction((ToastButton("Accept My Fate", "ok")))

    def callback():
        subprocess.call(["shutdown", "-r", "-t", "0"])

    def dismissed_callback():
        logging.info("Reboot cancelled by the user")

    start_toast_with_callback_thread(toast, callback=callback, dismissed_callback=dismissed_callback)


def time_consuming_function(bluepepper_app: BluePepperApp):
    logging.info("waiting 5 seconds (FastAPI)")
    time.sleep(5)
    logging.info("Done")
