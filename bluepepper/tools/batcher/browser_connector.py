from pathlib import Path

from lucent import Convention

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
    document: dict | None = None,
    document_id: str | None = None,
    document_name: str | None = None,
    convention: Convention | None = None,
    path: Path | None = None,
    documents: list[dict] | None = None,
    document_ids: list[str] | None = None,
    document_names: list[str] | None = None,
    paths: list[Path] | None = None,
):
    print("#" * 30)
    print(document_name)
    print(document_names)
    print(kwargs)
    # Check a few things
    if not script_path and not module:
        raise AttributeError("A Batcher Job needs at least a script or a module")
    if module and not function:
        raise AttributeError("Please provide a function to execute")

    # Get BatcherWidget
    batcher = get_batcher_widget(browser)

    # Format keyword arguments
    kwargs = kwargs or {}
    formatted_kwargs = {}
    for key, value in kwargs.items():
        formatted_kwargs[key] = value
        if value == "<document_name>":
            formatted_kwargs[key] = document_name

    # Create & send job
    job_data = JobData(
        name=name,
        description=description,
        script_path=script_path or Path(),
        script_args=script_args or [],
        module=module,
        func=function,
        kwargs=formatted_kwargs,
        priority=priority,
        notify_when_done=notify_when_done,
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
