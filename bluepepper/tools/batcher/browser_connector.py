from pathlib import Path

from bluepepper.app.main_window.main_window import BluePepperApp
from bluepepper.tools.batcher.batcher_widget import BatcherWidget
from bluepepper.tools.batcher.job_model import JobData
from bluepepper.tools.browser.browser_widget import BrowserWidget


def add_job(
    browser: BrowserWidget,
    name: str,
    description: str,
    script_path: Path | None = None,
    script_args: list[str] | None = None,
    module: str = "",
    function: str = "",
    kwargs: dict | None = None,
    priority: int = 50,
    notify_when_done: bool = False,
    notify_message: str = "",
):
    # Check a few things
    if not script_path and not module:
        raise AttributeError("A Batcher Job needs at least a script or a module")
    if module and not function:
        raise AttributeError("Please provide a function to execute")

    # Get BatcherWidget
    batcher = get_batcher_widget(browser)

    # Create & send job
    kwargs = kwargs or {}
    script_args = script_args or []
    job_data = JobData(
        name=name,
        description=description,
        script_path=script_path or Path(),
        script_args=script_args,
        module=module,
        func=function,
        kwargs=kwargs,
        priority=priority,
        notify_when_done=notify_when_done,
        notify_message=notify_message,
    )
    batcher._add_job(job_data)


def get_batcher_widget(browser: BrowserWidget) -> BatcherWidget:
    bluepepper_app: BluePepperApp = getattr(browser, "bluepepper_app")
    if not bluepepper_app:
        raise AttributeError("This Browser is not a child of a BluePepper App, you cannot create Batcher Jobs")

    for widget in bluepepper_app.page_widgets:
        if isinstance(widget, BatcherWidget):
            return widget

    raise RuntimeError("Batcher widget not found")
