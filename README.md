
# Table of Contents

- [What is BluePepper?](#what-is-bluepepper)
- [Video Tutorial](#video-tutorial)
- [Very Quick Start](#very-quick-start)
- [In-Depth Quick Start](#in-depth-quick-start)
- [Core Concepts](#core-concepts)
- [Configuration](#configuration)
  - [Project Settings](#project-settings)
  - [Database Configuration](#database-configuration)
    - [MongoDB Atlas Setup](#mongodb-atlas-setup)
  - [Lucent Configuration](#lucent-configuration)
  - [Browser Configuration](#browser-configuration)
    - [Browser Application Configuration](#browser-application-configuration)
      - [Entities](#entities)
      - [Tasks](#tasks)
      - [FileKinds](#kinds)
      - [Actions](#actions)
      - [Passing Arguments to Actions](#passing-arguments-to-actions)
      - [Filtering Tasks and Actions](#filtering-tasks-and-actions)
- [Design Philosophy](#design-philosophy)

# What is BluePepper?

BluePepper is a pipeline application designed for 2D/3D animation studios. The project aims to achieve several key goals:

- Provide a straightforward and lean pipeline application that is easy to configure and use
- Operate independently from production trackers or elaborate online services
- Make navigation and automation efficient and simple to set up
- Strike the best balance between ease of setup and automation capabilities : you'll need basic development skills, but adding new features should be reasonably straightforward

# Video Tutorials
Coming soon (hopefully)

# Very Quick Start
- Download the source code.
- Unzip it into a new folder, for example `myProject`.
- Run install_dev.bat.
- Double-click the newly created BluePepper shortcut.
- Feel free to fiddle with the files in the `conf` folder.

# In Depth Quick Start

Now that you've had a chance to test BluePepper quickly, let's dive into the details.

## Core Concepts

BluePepper relies on a few key features:

- **MongoDB Server**: Contains all the `Documents` for your project (primarily assets and shots). A `Document` is essentially the identity card of your assets and shots. Think of it as metadata that BluePepper uses for many of its features
- **Codex**: Allows you to declare all the naming conventions for your project (i.e., how files should be named, where they should be stored, which characters are allowed/forbidden). The codex uses the Python package [Lucent](https://pypi.org/project/lucent-codex/). For more information, see the [Lucent documentation](https://github.com/tristanlanguebien/lucent)
- **Browser**: Allows you to search for files using the `Database` and the `Codex` together. When you select a `Document` and a file type, you are effectively creating a file search that resolves the naming convention using the asset/shot document.
- **Batcher**: The task manager that executes in the background the actions you launch from the Browser. Although it's somewhat advanced to use, it's a powerful tool for running an action on hundreds of shots in a single click

Once you become familiar with these four components, a world of possibilities opens up to you!

## Setting up a development environment

- Fork the repository to your personal GitHub page (for example, `bluepepper_myProject`). This will make it easier to edit the configuration and deploy it to your team later
- Clone the repository
- Run `install_dev.bat`
- You can now open the app using the newly created BluePepper shortcut, but let's do some configuration first

## Configuring the Project

Edit the file `conf/project.py` so it matches you project's needs

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
In the `conf/database.py` file, several connection modes to a MongoDB database are available:

- **local**: Probably the best option if you just want to test BigPipe or if you only plan to use it on a personal project, but keep in mind that the server runs locally and only when the application is open (so this option is not suitable for collaborative work).

- **host-port**: If you or your IT department can set up a MongoDB server, this option will likely suit your needs.

- **uri**: If you do not know how to set up a MongoDB server yourself, the easiest solution is to use an online service that hosts it for you, and connect using the URI provided by that service.

## MongoDB Atlas Setup (Optional)

This section is intended for users who need help setting up a MongoDB server. If you do not need this, simply skip to the next section.

MongoDB Atlas allows you to host one database for free per account. Fortunately, we do not need a large database, so the free tier works perfectly well.

**Warning:** Keep in mind that the free tier does not include backups.

- Create an account at https://www.mongodb.com/products/platform/atlas-database
- Follow the welcome instructions, or go to  
  **Account → Organizations → {your organization} → All Projects → {your project} → Clusters → Build a Cluster**
- Choose the **Free** tier.
- Give your cluster a name (for example, `bluepepperDB`).
- Uncheck **"Preload sample dataset"**.
- Click **"Create Deployment"**.
- Set the admin password and store it somewhere safe.
- You may create an additional user if you want to fine-tune permissions  
  (go to **Clusters → Database & Network Access**. From there, you can set the user privileges to **"Read and write any database"** instead of **"Admin"**).
- Add the IP address `0.0.0.0/0` so the database can be accessed from anywhere on the internet.
- Your database is now up and running.
- Go to **Connect → Drivers → Python**, then copy the **SRV connection string**.
- Open `conf/database.py`.
- Set the mode to `"uri"`.
- Paste the connection string as the value for `"uri"`.
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
    uri: str | None = "mongodb+srv://user:password@my.server.mongodb.net"
```

BluePepper should now be able to connect to the MongoDB Atlas database.

Feel free to create an asset and a shot in BluePepper to see how the database is structured.
You can browse your database in **MongoDB Atlas → Clusters → Browse Collections.**

Alternatively, you can use a dedicated app, such as [MongoDB Compass](https://www.mongodb.com/products/tools/compass).

## Configuring the naming conventions

In the file `conf/naming_conventions.py`, you can configure all the naming conventions for your project.

To keep things short, you just have to know that Lucent holds everything together within a Codex, which contains Conventions (string templates made up of fields) and Rules (that define how fields should behave). For more information, consult the official documentation: [Lucent Documentation](https://github.com/tristanlanguebien/lucent).

`naming_conventions.py` comes with a few boilerplate examples that show the various features of Lucent, but you can go for something simpler. Here is a minimal version of the Codex:

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
    asset_modeling_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "mdl", "extension" : ".blend"})

    # Shots
    shot_work_dir = Convention("{@project_root}/shots/{shot}")
    shot_workfile = Convention("{@shot_work_dir}/{shot}_{task}_v{version}.{extension}")
    shot_animation_workfile = Convention("{@shot_workfile}", fixed_fields={"task": "anim", "extension": ".blend"})


class BluePepperCodex(Codex):
    convs: BluePepperConventions = BluePepperConventions()
    rules: BluePepperRules = BluePepperRules()


codex = BluePepperCodex()
```

Be careful though: the Browser's configuration relies on Conventions as well. If you remove a Convention that is used by the Browser, BluePepper won't be able to boot anymore. Worry not, we will cover all of that in the next section.

## Configuring the Browser

Here is how the Browser is structured:

BrowserConfig -> Entities -> Tasks -> FileFileKinds -> Files.

First, `Entities` define which database collections that the user should be able to browse. The obvious ones are assets and shots, but you may want to create other entities (episodes, levels...)

`Entities` can now be filled with `Tasks`. In the context of the browser, you can think of `Tasks` as a convinient way to regroup files kinds together.

`Tasks` are then filled with `FileFileKinds`, which is basically a Lucent `Convention`.

`Files` are the result of a file discovery that matches the selected `Documents` and the selected `FileFileKind`

### Entities

The base point here is to create a new config

```python
config = AppConfig("bigBrowserMainApp")
```

First, you need to declare the entities you want to access (typically, assets and shots). Adding an entity automatically adds a tab to the interface:

```python
asset_entity = Entity(name="asset", collection="assets", filters=["type"])
config.add_entity(asset_entity)
```

The `collection` parameter indicates which collection in your database the Browser will query for documents. By default, BluePepper uses only the `assets` and `shots` collections, but depending on your needs, you might want to create additional entities and corresponding collections in MongoDB.

Keep in mind that the filters must be coherent with what you have defined into `naming_conventions.py` : for instance, the Browser will not be able to create an "episode" filter if you got rid of the "episode" field in your Codex.

The documents in the database under the provided collection will now appear in the first column of the interface, and the filtering options will be available at the top.

### Tasks

Next, you can create tasks within your entity. Tasks are simply a way to group your file kinds to match your departments' needs:

```python
asset_modeling_task = Task("modeling")
asset_entity.add_task(asset_modeling_task)
```

The created tasks will appear in the second column of the interface.

### FileKinds

You can now populate your tasks with kinds. FileKinds are essentially a way to access files that match a specific convention from your project's codex:

```python
kind = FileKind(
    name="asset_modeling_workfile_blender",
    label="Workfile (blender)",
    convention=codex.convs.asset_modeling_workfile_blender,
)
asset_modeling_task.add_kind(kind)
```

FileKinds will appear in the third column of the interface.

#### Actions

Contextual menu actions can be added to documents, kinds, and files, allowing you to define which specific actions can be run when you right-click on various elements of the interface.

For example:

1. Create a new file in `conf/scripts` (for example, `print_stuff.py`)
2. Create a new function in this file:

```python
def say_hello() -> None:
    print("Hello World")
```

3. Add an action that runs this function using this code:

```python
action = MenuAction(
    label="say hello",
    module="conf.scripts.print_stuff",
    callable="say_hello",
)
asset_entity.add_document_action(action)
```

When you right-click on an asset document, the "say hello" action should appear, and "Hello World" should be printed to the console when you click on it.

#### Passing Arguments to Actions

Printing "Hello World" is nice, but what if you need to pass the selected documents or files as arguments?

You can use the `kwargs` attribute with these specific keywords, which will be replaced when passed to your functions:

- `<document>`: Each of the selected documents (triggers the function once per document)
- `<documents>`: List of all selected documents (triggers the function once)
- `<document_name>`: Each of the selected documents' names (triggers the function once per document)
- `<document_names>`: List of all documents' names (triggers the function once)
- `<document_id>`: Each of the selected documents' MongoDB IDs (triggers the function once per document)
- `<document_ids>`: List of all documents' MongoDB IDs (triggers the function once)
- `<convention>`: The selected convention object
- `<path>`: Each selected path (triggers the function once per path)
- `<paths>`: List of all selected paths (triggers the function once)
- `<browser>`: The BrowserWidget object

You may wonder why there are so many similar keywords like `document` and `documents`. There's actually an important difference. Let's say you have 10 selected documents:

- Using `<document>` triggers the function 10 times, once for each document
- Using `<documents>` triggers the function only once, with the list of documents passed as an argument (assuming your function contains a loop)

The same logic applies to `<document_name(s)>`, `<document_id(s)>`, and `<path(s)>`.

#### Filtering Tasks and Actions

What if the rigging task should only appear on character assets? What if an action should only work on MP4 files? Filters have you covered.

There are two types of filters:

- `doc_filter`: Depends on the document
- `path_filter`: Depends on the path

Create a function that returns `True` if your condition is met, `False` otherwise. Here are some examples: 

```python
# Task "Rigging" will only appear if a character is selected
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

What if you have both a character and a prop selected? The Browser handles this intelligently—the menu action will show, but it will only execute on documents that match your filter.

# Design Philosophy

BluePepper makes minimal use of complex software architecture, which is generally considered a best practice. However, modular architectures can be difficult to code, test, update, and deploy.

BluePepper's structure is intentionally simple: you download the source code, run the installer, and it works.

Several design choices were made to simplify BluePepper's architecture:

- **Python Configuration Files**: BluePepper could use JSON, YAML, or TOML for configuration files, but Python files unlock two important capabilities: the ability to configure BluePepper more organically (if/else statements, access to environment variables, etc.) rather than with just static values
- **One Repository = One Project**: You'll notice that BluePepper has a single `conf` folder. This is intentional. We believe that BluePepper's greatest strength is its simplicity of use
- **Minimal Use of Plugins/Entry Points**: If you want to add features to BluePepper, you simply create a new Python module, import it, and it works

These choices aim to:

- Lower the barrier to entry for development, particularly for technical directors and tech artists who may not have sufficient experience with complex software architectures
- Provide excellent development ergonomics: autocompletion at every level, easy configuration
- Reduce side effects, making it safe to deploy BluePepper to your colleagues without excessive fear of breaking something
