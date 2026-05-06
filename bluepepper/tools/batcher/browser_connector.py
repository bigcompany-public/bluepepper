from pathlib import Path

from bluepepper.tools.batcher.job_model import JobData
from bluepepper.tools.browser.browser_widget import BrowserWidget, get_batcher_widget


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
    batcher.add_job(job_data)
