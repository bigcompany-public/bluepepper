"""
This module contains all functions susceptible to be called for bluepepper's main window
All of them have the BluePepperApp instance as first argument
"""

import logging
import os
import subprocess
import time

from bluepepper.app.main_window.main_window import BluePepperApp
from bluepepper.toast import start_toast_with_callback_thread
from windows_toasts import Toast, ToastButton


def close(bluepepper_app: BluePepperApp):
    logging.info("Closing BluePepper App (FastAPI)")
    toast = Toast(["BluePepper will now close"])
    toast.AddAction((ToastButton("Not Now", "cancel")))
    toast.AddAction((ToastButton("Ok", "ok")))

    def callback():
        os._exit(0)

    def dismissed_callback():
        logging.info("BluePepper closing cancelled by the user")

    start_toast_with_callback_thread(
        toast, callback=callback, dismissed_callback=dismissed_callback
    )


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


def reboot(bluepepper_app: BluePepperApp):
    logging.info("Rebooting computer (FastAPI)")

    toast = Toast(["BluePepper will now restart your computer"])
    toast.AddAction((ToastButton("Cancel Shutdown", "cancel")))
    toast.AddAction((ToastButton("Accept My Fate", "ok")))

    def callback():
        subprocess.call(["shutdown", "-r", "-t", "0"])

    def dismissed_callback():
        logging.info("Reboot cancelled by the user")

    start_toast_with_callback_thread(
        toast, callback=callback, dismissed_callback=dismissed_callback
    )


def time_consuming_function(bluepepper_app: BluePepperApp):
    logging.info("waiting 5 seconds (FastAPI)")
    time.sleep(5)
    logging.info("Done")
