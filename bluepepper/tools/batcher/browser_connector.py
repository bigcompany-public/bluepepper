import re
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
    # The following arguments are used for kwargs resolution
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
    # Check a few things
    if not script_path and not module:
        raise AttributeError("A Batcher Job needs at least a script or a module")
    if module and not function:
        raise AttributeError("Please provide a function to execute")

    # Get BatcherWidget
    batcher = get_batcher_widget(browser)

    # Format module keyword arguments
    local_vars = locals()
    kwargs = kwargs or {}
    formatted_kwargs = {}
    for key, value in kwargs.items():
        formatted_kwargs[key] = value
        if not isinstance(value, str):
            continue
        if value.startswith("<") and value.endswith(">"):
            var_name = value[1:-1]
            if var_name in local_vars:
                formatted_kwargs[key] = local_vars[var_name]

    # Format script arguments
    script_args = script_args or []
    formatted_args = []
    for arg in script_args:
        if isinstance(arg, str) and arg.startswith("<") and arg.endswith(">"):
            var_name = arg[1:-1]
            if var_name in local_vars:
                arg = local_vars[var_name]
        formatted_args.append(arg)

    # Format job name & description
    def substitute_special_keywords(match: re.Match) -> str:
        token = match.group(0)
        var_name = token[1:-1]
        if var_name in local_vars:
            if not local_vars[var_name]:
                return token
            return str(local_vars[var_name])
        return token

    name = re.sub(r"<[a-z_]+>", repl=substitute_special_keywords, string=name)
    description = re.sub(r"<[a-z_]+>", repl=substitute_special_keywords, string=description)

    # Create & send job
    job_data = JobData(
        name=name,
        description=description,
        script_path=script_path or Path(),
        script_args=formatted_args,
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
