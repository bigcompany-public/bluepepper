# Table of Contents

- [What is BluePepper?](#what-is-bluepepper)
- [Video Tutorials](#video-tutorials)
- [Very Quick Start](#very-quick-start)
- [In-Depth Quick Start](#in-depth-quick-start)
- [Core Concepts](#core-concepts)
- [Configuration](#configuration)
  - [Project Settings](#configuring-the-project)
  - [Database Configuration](#configuring-the-database)
    - [MongoDB Atlas Setup](#mongodb-atlas-setup-optional)
  - [Naming Conventions](#configuring-the-naming-conventions)
  - [Browser Configuration](#configuring-the-browser)
    - [Entities](#entities)
    - [Tasks](#tasks)
    - [FileKinds](#filekinds)
    - [Actions](#actions)
    - [Passing Arguments to Actions](#passing-arguments-to-actions)
    - [Filtering Tasks and Actions](#filtering-tasks-and-actions)
    - [Adding Icons to Menu Actions](#adding-icons-to-menu-actions)
    - [Creating a Batcher Job through a MenuAction](#creating-a-batcher-job-through-a-menuaction)
  - [Launcher Configuration](#launcher-configuration)
    - [About Qt Dialogs](#about-qt-dialogs)
    - [About Beautiful Qt Dialogs](#about-beautiful-qt-dialogs)
- [Design Philosophy](#design-philosophy)

---

# What is BluePepper?

BluePepper is a pipeline application designed for 2D/3D animation studios. The project aims to achieve several key goals:

- Provide a straightforward and lean pipeline application that is easy to configure and use
- Operate independently from production trackers or elaborate online services
- Make navigation and automation efficient and simple to set up
- Strike the best balance between ease of setup and automation capabilities. You will need basic development skills, but adding new features should be reasonably straightforward

# Video Tutorials

Coming soon (hopefully).

# Very Quick Start

- Download the source code.
- Unzip it into a new folder, for example `myProject`.
- Run `install_dev.bat`.
- Double-click the newly created BluePepper shortcut.
- Feel free to explore the files in the `conf` folder.

# In-Depth Quick Start

Now that you have had a chance to test BluePepper, let's dive into the details.

## Core Concepts

BluePepper relies on a few key components:

- **MongoDB Server**: Contains all the `Documents` for your project (primarily assets and shots). A `Document` is essentially the identity card of an asset or shot, think of it as metadata that BluePepper uses across many of its features.
- **Codex**: Allows you to declare all the naming conventions for your project (i.e., how files should be named, where they should be stored, and which characters are allowed or forbidden). The Codex uses the Python package [Lucent](https://pypi.org/project/lucent-codex/). For more information, refer to the [Lucent documentation](https://github.com/tristanlanguebien/lucent).
- **Browser**: Allows you to search for files by combining the `Database` and the `Codex`. When you select a `Document` and a file type, you are effectively creating a file search that resolves the naming convention using the asset or shot document.
- **Batcher**: The task manager that executes in the background the actions you launch from the Browser. While it is somewhat advanced, it is a powerful tool for running an action across hundreds of shots in a single click.

Once you are familiar with these four components, a world of possibilities opens up!

## Setting Up a Development Environment

- Fork the repository to your personal GitHub page (for example, `bluepepper_myProject`). This will make it easier to edit the configuration and deploy it to your team later.
- Clone the repository.
- Run `install_dev.bat`.
- You can now open the app using the newly created BluePepper shortcut, but let's do some configuration first.

## Configuring the Project

Edit the file `conf/project.py` to match your project's needs:

```python
class ProjectSettings:
    project_name: str = "MyIncredibleProject"
    project_code: str = "proj"
    width: int = 1920
    height: int = 1080
    fps: float = 25.0
    start_frame: int = 101
    production_trackers: List[str] = []
```

## Configuring the Database

In the `conf/mongodb.py` file, several connection modes to a MongoDB database are available:

- **local**: Probably the best option if you just want to test BluePepper or use it on a personal project. Keep in mind, however, that the server runs locally and only while the application is open. This option is not suitable for collaborative work.
- **host-port**: If you or your IT department can set up a dedicated MongoDB server, this option will likely suit your needs.
- **uri**: If setting up a MongoDB server yourself is not an option, the easiest solution is to use an online hosting service and connect using the URI it provides.

## MongoDB Atlas Setup (Optional)

This section is intended for users who need help setting up a MongoDB server. If this does not apply to you, feel free to skip to the next section.

MongoDB Atlas allows you to host one database for free per account. Since BluePepper does not require a large database, the free tier works perfectly well.

**Warning:** Keep in mind that the free tier does not include backups.

- Go to https://www.mongodb.com/products/platform/atlas-database and click `Get Started` to create an account.
- Follow the welcome instructions, or navigate to
  **Account → Organizations → {your organization} → All Projects → Project 0 → Project Overview → Create**
- On the next page:
    - Choose the **Free** tier.
    - Give your cluster a name (for example, `bluepepperDB`).
    - Uncheck **"Preload sample dataset"**.
    - Click **"Create Deployment"**.
![MongoDB Free Plan](docs/img/mongodb_free.jpg)

- MongoDB will ask for an admin password. Set it and store it somewhere safe.
![MongoDB Admin User](docs/img/mongodb_admin_user.jpg)
- Next, MongoDB will ask for a connection method. Select **Drivers → Python**, uncheck **"SRV Connection String"** and **Show Password**, then copy the **Connection String** and keep it somewhere safe. (Note: the SRV connection string relies on a DNS server, which may fail on VPN networks.)
![MongoDB Connection String](docs/img/mongodb_connection_string.jpg)
- You may create an additional user if you wish to fine-tune permissions. Under the **Security** section, go to **Database & Network Access**, where you can create a new database user and set its privileges to **"Read and write any database"** instead of **"Admin"**.
![MongoDB User1](docs/img/mongodb_network_access.jpg)
![MongoDB User1](docs/img/mongodb_new_user.jpg)
![MongoDB User1](docs/img/mongodb_new_user2.jpg)
- For now the database will only be allowed for your IP address. To allow the database to be accessed from anywhere on the internet:
    - In **Database & Network Access**, go to **IP Access List**
    - Add the IP address `0.0.0.0/0`
![MongoDB User1](docs/img/mongodb_new_ip.jpg)
![MongoDB User1](docs/img/mongodb_new_ip2.jpg)

Now that your database is now up and running, open `conf/mongodb.py`.
- Set the mode to `"uri"`.
- Paste the connection string as the value for `"uri"` (don't forget to set the proper username and password).
- Save the file.

```python
@dataclass(frozen=True)
class DatabaseSettings:
    database_name: str = "myProjectDB"
    mode: str = "uri"
    host: str = "127.0.0.1"  # Won't be used
    port: int = 27017  # Won't be used
    user: str | None = None  # Won't be used
    password: str | None = None  # Won't be used
    uri: str | None = "mongodb://<db_username>:<db_password>@..."
```

BluePepper should now be able to connect to your MongoDB Atlas database.

Feel free to create an asset and a shot in BluePepper to see how the database is structured. You can browse your database via **MongoDB Atlas → Clusters → Browse Collections**, or use a dedicated application such as [MongoDB Compass](https://www.mongodb.com/products/tools/compass).

![MongoDB User1](docs/img/mongodb_create_asset.jpg)
![MongoDB User1](docs/img/mongodb_create_asset2.jpg)
![MongoDB User1](docs/img/mongodb_create_asset3.jpg)

## Configuring the Naming Conventions

In the file `conf/naming_conventions.py`, you can configure all the naming conventions for your project.

In brief: Lucent organises everything within a `Codex`, which contains `Conventions` (string templates made up of fields) and `Rules` (which define how fields should behave). For more information, consult the [Lucent documentation](https://github.com/tristanlanguebien/lucent).

`naming_conventions.py` comes with a few boilerplate examples demonstrating the various features of Lucent, but you can keep things simple. Here is a minimal version of the Codex:

```python
from lucent import Codex, Convention, Conventions, Rule, Rules

class BluePepperRules(Rules):
    default = Rule(r"[a-zA-Z0-9]+")
    asset = Rule(r"([a-z]+)([A-Z][a-z]*)*", examples=["peach", "redApple", "philip", "cassie"])
    type = Rule(r"[a-z]+", examples=["prp", "chr", "elem"])
    sequence = Rule(r"sq\d{3}", examples=["sq001"])
    shot = Rule(r"sh\d{4}[A-Z]?", examples=["sh0010", "sh0010A"])
    version = Rule(r"\d{3}", examples=["001", "002", "003"])

class BluePepperConventions(Conventions):
    # Project
    project_root = Convention("D:/projects/my_project")

    # Configuration for entity creation
    asset_fields = Convention("{type}_{asset}")
    asset_identifier = Convention("{asset}")
    shot_fields = Convention("{sequence}_{shot}")
    shot_identifier = Convention("{shot}")

    # Assets
    asset_work_dir = Convention("{@project_root}/assetWorkspace/{type}/{asset}")
    asset_workfile = Convention("{@asset_work_dir}/{asset}_{task}_v{version}.{extension}")
    asset_modeling_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "mdl", "extension" : "blend"})

    # Shots
    shot_work_dir = Convention("{@project_root}/shots/{shot}")
    shot_workfile = Convention("{@shot_work_dir}/{shot}_{task}_v{version}.{extension}")
    shot_animation_workfile = Convention("{@shot_workfile}", fixed_fields={"task": "anim", "extension": "blend"})


class BluePepperCodex(Codex):
    convs: BluePepperConventions = BluePepperConventions()
    rules: BluePepperRules = BluePepperRules()


codex = BluePepperCodex()
```

One important note: the Browser's configuration also relies on Conventions. If you remove a Convention that is used by the Browser, BluePepper will not be able to start. Don't worry, this is covered in the next section.

## Configuring the Browser

The Browser is structured as follows:

`BrowserConfig` → `Entities` → `Tasks` → `FileKinds` → `Files`

**Entities** define which database collections the user can browse. The obvious ones are assets and shots, but you may want to create additional entities (episodes, levels, etc.).

**Tasks** group file kinds together within an entity, think of them as a convenient way to organise files by department.

**FileKinds** are essentially a Lucent `Convention`, they define which specific files should be surfaced in the Browser.

**Files** are the result of a file discovery that matches the selected `Documents` against the selected `FileKind`.

The Browser is configured through the file `conf/app_browser.py`. Similar to the file `conf/naming_conventions.py`, it will contain a lot of examples for demonstration purposes. In the following sections, we'll see how to create it from scratch.

Clear out the file `conf/app_browser.py` and create a blank AppConfig inside a function `get_tool_config()`. We will also import everything we need later on.

```python
from pathlib import Path
from bluepepper.core import codex
from bluepepper.tools.browser.browser_config import (
    AppConfig,
    Entity,
    FileKind,
    MenuAction,
    Task,
)


def get_tool_config() -> AppConfig:
    config = AppConfig("bigBrowserMainApp")
    return config
```

### Entities

Declare the entities you want to access (typically assets and shots). Adding an entity automatically adds a tab to the interface:

```python
asset_entity = Entity(name="asset", collection="assets", filters=["type"])
config.add_entity(asset_entity)
```

The `collection` parameter indicates which MongoDB collection the Browser will query for documents. By default, BluePepper uses the `assets` and `shots` collections, but you can create additional entities and corresponding collections as needed.

Note that filters must be consistent with what you have defined in `naming_conventions.py`. For instance, the Browser will not be able to create an "episode" filter if the "episode" field does not exist in your Codex.

Documents from the specified collection will appear in the first column of the interface, with filtering options available at the top.

### Tasks

You can now create tasks within your entity. Tasks are a way to group file kinds according to your departments' needs:

```python
asset_modeling_task = Task("modeling")
asset_entity.add_task(asset_modeling_task)
```

Tasks appear in the second column of the interface.

### FileKinds

Populate your tasks with file kinds. A `FileKind` provides access to files matching a specific convention from your project's Codex:

```python
kind = FileKind(
    name="asset_modeling_workfile",
    label="Workfile",
    convention=codex.convs.asset_modeling_workfile,
)
asset_modeling_task.add_kind(kind)
```

FileKinds appear in the third column of the interface. When selecting a `Document` and a `FileFind` the result of a file discovery appears in the fourth column of the interface.

#### Result
Before going further, we should take a look at the result. Here is the full code so far:

```python
from bluepepper.core import codex
from bluepepper.tools.browser.browser_config import (
    AppConfig,
    Entity,
    FileKind,
    Task,
    MenuAction
)


def get_tool_config() -> AppConfig:
    config = AppConfig("bigBrowserMainApp")
    asset_entity = Entity(name="asset", collection="assets", filters=["type"])
    config.add_entity(asset_entity)
    asset_modeling_task = Task("modeling")
    asset_entity.add_task(asset_modeling_task)
    kind = FileKind(
        name="asset_modeling_workfile",
        label="Workfile (blender)",
        convention=codex.convs.asset_modeling_workfile,
    )
    asset_modeling_task.add_kind(kind)
    return config
```

When opening the Browser, you can see the result:
1. There is a single "Asset" tab
2. Assets can be filtered by type
3. The first column displays the available assets
4. The Modeling task is available
5. And contains a Workfile task
6. While there is still no file on the server right now, the console shows that the Browser is actively looking for files that match the naming convention.
![Browser Config](docs/img/browser_config.jpg)

#### Actions

Contextual menu actions can be added to documents, kinds, and files, allowing you to define which actions are available when right-clicking on various elements of the interface.

For example:

- Create a new file in `conf/scripts` (for example, `print_stuff.py`)
- Define a function in that file:

```python
def say_hello() -> None:
    print("Hello World")
```

- In `conf/app_browser.py`, add an action that calls this function:

```python
action = MenuAction(
    label="say hello",
    module="conf.scripts.print_stuff",
    callable="say_hello",
)
asset_entity.add_document_action(action)
```

When you right-click on an asset document, the "say hello" action should appear, and "Hello World" will be printed to the console when you click it.

![Browser Config](docs/img/browser_action.jpg)

#### Passing Arguments to Actions

Printing "Hello World" is a fine start, but what if you need to pass the selected documents or files as arguments?

As an example, we will add a new function to `print_stuff.py`

```python
def print_selection(selection):
    print(selection)
```

And add these lines to `app_browser.py`

```python
action = MenuAction(
    label="print document",
    module="conf.scripts.print_stuff",
    callable="print_selection",
    kwargs={"selection": "<document>"}
)
asset_entity.add_document_action(action)
```

Now, see the result, with two documents selected:

![Browser Config](docs/img/browser_action2.jpg)

You can use the `kwargs` attribute with all the following special keywords, which are automatically substituted when passed to your functions:

- `<document>`: Each of the selected documents (triggers the function once per document)
- `<documents>`: List of all selected documents (triggers the function once)
- `<document_name>`: Each of the selected documents' names (triggers the function once per document)
- `<document_names>`: List of all selected documents' names (triggers the function once)
- `<document_id>`: Each of the selected documents' MongoDB IDs (triggers the function once per document)
- `<document_ids>`: List of all selected documents' MongoDB IDs (triggers the function once)
- `<convention>`: The selected convention object
- `<path>`: Each selected path (triggers the function once per path)
- `<paths>`: List of all selected paths (triggers the function once)
- `<browser>`: The BrowserWidget object

You may wonder why there are both singular and plural variants like `<document>` and `<documents>`. The distinction is significant. With 10 selected documents:

- `<document>` triggers the function 10 times, once per document
- `<documents>` triggers the function once, passing the entire list as an argument (assuming your function contains a loop)

The same logic applies to `<document_name(s)>`, `<document_id(s)>`, and `<path(s)>`.

Let's show this subtle difference with an example

```python
action = MenuAction(
    label="print documentS",
    module="conf.scripts.print_stuff",
    callable="print_selection",
    kwargs={"selection": "<documents>"}
)
asset_entity.add_document_action(action)
```

As explained, the result is now printed as a list, instead of printing the documents one by one.

![Browser Config](docs/img/browser_action3.jpg)

#### Filtering Tasks and Actions

What if the rigging task should only appear for character assets? What if an action should only work on MP4 files? Filters have you covered.

There are two types of filters:

- `doc_filter`: Depends on the document
- `path_filter`: Depends on the path

Create a function that returns `True` if your condition is met, `False` otherwise. Here are some examples:

```python
# Task "Rigging" will only appear if a character asset is selected
def is_chr(doc: dict) -> bool:
    if not is_asset(doc):
        return False
    return doc["type"] == "chr"


asset_rigging_task = Task("rigging", doc_filter=is_chr)
asset_entity.add_task(asset_rigging_task)


# Action "Open in VLC" will only appear on MP4 files
def is_mp4(path: Path) -> bool:
    return path.suffix == ".mp4"


action = MenuAction(
    label="Show in VLC",
    module="...",
    callable="...",
    kwargs={"path": "<path>"},
    path_filter=is_mp4,
)
```

What if you have both a character and a prop selected? The Browser handles this gracefully. The menu action will appear, but it will only execute on documents that match your filter.

#### Adding Icons to Menu Actions

BluePepper uses QtAwesome for its menu icons. To browse available icons, open a powershell terminal from the Launcher and run the command:

```powershell
qta-browser
```

![qta browser](docs/img/qta_browser.jpg)

From there, you can copy the icon code and use it when declaring your `MenuAction`. You can also set a custom colour if you wish:

```python
action = MenuAction(
    label="say hello",
    module="conf.scripts.print_stuff",
    callable="say_hello",
    qta_icon="mdi6.hand-wave",
    qta_icon_color="#FF0000"
)
```

![qta browser](docs/img/browser_icon.jpg)

#### Creating a Batcher Job through a MenuAction

*(Coming soon. the Batcher feature has not been released yet.)*

## Launcher Configuration

Let's add a simple icon to the Launcher that opens VLC.

First, create a file, for instance, `conf/scripts/vlc.py`:

```python
import os

def open_vlc():
    os.startfile("C:/Program Files/VideoLAN/VLC/vlc.exe")
```

Then open `conf/app_launcher.py` and append an item to the `apps` list:

```python
class DefaultLauncherConfig(LauncherConfig):
    apps: list[LauncherItem] = [
        LauncherItem(
            label="VLC",
            icon="software_vlc.png",  # all icons are stored in bluepepper/gui/icons
            module="conf.scripts.vlc",
            function="open_vlc",
            tooltip="Opens VLC",
        ),
    ]
```

A new app icon will appear in the Apps section of the Launcher, and VLC will open when you double-click it. Note that there is no technical difference between apps and tools, it is simply a convenient way to organise your icons. If you wanted the VLC icon to appear at the bottom of the Launcher, you would add the `LauncherItem` to `tools` instead of `apps`.

This approach to launching applications through custom functions gives you a great deal of flexibility from simple one-liners to complex launch sequences. See `maya_launcher.py` for a more involved example.

### About Qt Dialogs

BluePepper uses PySide6 for its interface, so you can open your own Qt Dialogs from the Launcher. Let's create one in a new file `conf/scripts/open_dialog.py`:

```python
# BluePepper uses qtpy to wrap around PySide6 and PySide2
from qtpy.QtWidgets import QDialog, QPushButton, QVBoxLayout

class HelloDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.button = QPushButton("Say Hello")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.say_hello)

    def say_hello(self):
        print("hello")

def show_dialog():
    dialog = HelloDialog()
    dialog.exec()
```

Then add it to the Launcher:

```python
apps: list[LauncherItem] = [
    LauncherItem(
        label="Hello Dialog",
        icon="console.png",
        module="conf.scripts.open_dialog",
        function="show_dialog",
        tooltip="Demo Qt Dialog",
    )
]
```

### About Beautiful Qt Dialogs

The dialog above is rather plain. BluePepper provides custom Qt widgets and dialogs to apply the correct stylesheet and ensure a consistent look across the application.

Here is a polished version of `open_dialog.py`:

```python
from qtpy.QtWidgets import QPushButton, QVBoxLayout, QWidget

from bluepepper.gui.utils import get_qta_icon
from bluepepper.gui.widgets.container import (
    ContainerDialog,
    ContainerWidget,
    get_qt_app,
)


class HelloWidget(QWidget):  # QWidget instead of QDialog
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.button = QPushButton("Say Hello")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.say_hello)

    def say_hello(self):
        print("hello")


def show_dialog():
    app = get_qt_app()
    icon = get_qta_icon(name="mdi.tag-text", scale_factor=1.25)
    widget = HelloWidget()
    container = ContainerWidget(widget=widget, icon=icon, title="Tag Manager")
    dialog = ContainerDialog(container)
    dialog.exec()
```

The result will be identical in functionality, but with considerably more style. If you need a reminder on how to use QtAwesome icons, see [Adding Icons to Menu Actions](#adding-icons-to-menu-actions).

# Design Philosophy

BluePepper makes minimal use of complex software architecture. While modular architectures are often considered best practice, they can be difficult to code, test, update, and deploy.

BluePepper's structure is intentionally simple: you download the source code, run the installer, and it works.

Several design choices were made to keep things lean:

- **Python Configuration Files**: BluePepper could use JSON, YAML, or TOML for configuration, but Python files unlock two important capabilities: the ability to configure the application more organically (using if/else statements, environment variable access, etc.) rather than being limited to static values.
- **One Repository = One Project**: BluePepper has a single `conf` folder, and this is intentional. We believe that simplicity is BluePepper's greatest strength.
- **Minimal Use of Plugins/Entry Points**: If you want to add features to BluePepper, you simply create a new Python module, import it, and it works.

These choices aim to:

- Lower the barrier to entry for development, particularly for technical directors and tech artists who may not have extensive experience with complex software architectures
- Provide excellent development ergonomics: autocompletion at every level, straightforward configuration
- Reduce side effects, making it safe to deploy BluePepper to your colleagues without undue risk of breaking anything
