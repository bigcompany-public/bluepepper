
# Table of Contents
- [What is BluePepper?](#what-is-bluepepper)
- [Video Tutorial](#video-tutorial)
- [Very Quick Start](#very-quick-start)
- [Quick Start](#quick-start)
  - [MongoDB](#mongodb)

# What is BluePepper?
BluePepper is a pipeline application designed for 2D/3D animation studios.
The project has several goals:
- straightforward and lean pipeline app, easy to configure and easy to use
- does not rely on a production tracker, or elaborate online services.
- making navigation and automation efficient and easy to setup
- aimed at hitting the best compromise between ease to set up and extent to which you will be able to automate stuff : you will need basic development skills, but adding new features should be reasonably easy.

# Video Tutorial
Coming soon (hopefully)

# Very Quick Start
- download the source code
- Unzip it into a new folder, for instance `myProject`
- run install_dev.bat
- Double click on the newly created BluePepper shortcut
- Feel free to fiddle with the files within the conf folder.

# Concepts

Maintenant que vous avez pu essayer rapidement BluePepper, rentrons un peu dans les détails.
BluePepper repose sur quelques fonctionnalités clé :
- Un serveur mongoDB, qui contient tous les documents de votre projet (essentiellement les assets et les shots). Qu'est ce qu'un document ? vous pouvez voir ça comme la carte d'identité de vos assets et de vos shots, utilisées par plein de fonctionnalités de BluePepper.
- Un `codex` qui permet de déclarer toutes les nomenclatures de votre projet (aka: comment les fichiers doivent se nommer, où ils doivent être rangés, quels characteres sont autorisés/interdits). le codex utilise le package python Lucent. vous pouvez consulter la documentation de lucent ici pour plus d'informations : [Documentation Lucent]https://github.com/tristanlanguebien/lucent
- Un Browser, qui permet de rechercher des fichier, en utilisant conjointement la base de données et les nomenclatures. Lorsque vous selectionnez un asset et un `file kind`, vous "construisez" une recherche de fichier.
- un Batcher, qui est le gestionnaire de tache qui execute en tache de fond les actions que vous lancez depuis le Browser. Bien que son utilisation soit un peu avancée, c'est un outil puissant pour lancer une action sur des centaines de shots en un clic!

Une fois que vous serez familiarisés avec ces quatres-là, un monde de possibles s'ouvre à vous !

# In Depth Quick start
- Fork the repository to your personal github page (for instance bluepepper_myProject). This will make editing the configuration and deploying it to your team easier down the line.
- run install_dev.bat
- At this point, you should be able to open the app, using the newly created BluePepper shortcut, but we'll do a little bit of configuration first.

## Project

dans le fichier conf/project.py, configurer les différents attributs pour qu'il correspondent avec vos besoins (project_name, frame rate...)

class ProjectSettings:
    project_name: str = "MyIncredibleProject"
    project_code: str = "proj"
    width: int = 1920
    height: int = 1080
    fps: float = 25.0
    start_frame: int = 101
    production_trackers: List[str] = []

## Database
Dans le fichier conf/database.py, plusieurs modes de connexion à une base de données mongodb sont disponibles:
- local : Certainement la meilleure option si vous voulez juste tester BigPipe, mais gardez à l’esprit que le serveur tourne en local, et seulement quand l’application est ouverte (cette option n’est donc pas adaptée pour travailler à plusieurs)

- host-port : Vous ou votre département IT pouvez mettre en place un serveur MongoDB ? cette option vous conviendra certainement.

- Si vous ne savez pas comment mettre en place un serveur mongoDB vous-même, le plus simple est d’utiliser un service en ligne qui le fera à votre place, et d’utiliser l’uri fournie via ce mode de connexion.

### MongoDB Atlas
Cette section est destinée aux utilisateurs qui ont besoin d'aide pour mettre en place un serveur mongodb. If you dont, just skip to the next section.

MongoDB Atlas propose d'heberger gratuitement une base de donnée par compte. Heureusement, nous n'avons pas besoin d'une base de donnée volumineuse, donc la version gratuite fera très bien l'affaire.
Warning : keep in mind the free offer doesnt have backups

- Créez un compte sur https://www.mongodb.com/products/platform/atlas-database
- Suivez les instructions de bienvenue, ou allez dans account -> organizations -> {your organization} -> All Projects -> {your project} -> Clusters -> Build a cluster
- chose the Free program
- Give your cluster a name (lets say "bluepepperDB")
- Uncheck "Preload sample dataset"
- Click "Create Deployment"
- Edit the admin password and keep it somewhere safe
- You may create an additional user, if you want to fine tune permissions (which will be in Clusters -> Database & Network Access. From here, you will be able to set the user privileges to "Read and write any database" instead of "Admin")
- Add the ip address 0.0.0.0/0, so the database can be accessed from anywhere on the internet
- Your database is up and running. 
- Now go to Connect -> Drivers -> Python -> copy the srv connection string
- Go to conf/database.py
- Set the mode to "uri"
- Paste the connection string as a value for "uri"
- save

@dataclass(frozen=True)
class DatabaseSettings:
    database_name: str = "bluepepper"
    mode: str = "uri"
    host: str = "127.0.0.1"
    port: int = 27017
    user: str | None = None
    password: str | None = None
    uri: str | None = "mongodb+srv://user:password@my.server.mongodb.net"

BluePepper should now be able to reach the MongoDB Atlas database !

Feel free to create an asset and a shot in BluePepper, to see how the database is structured. You can access your database in MongoDB Atlas -> Clusters -> Browse Collections

## Configuring the Browser

As stated in the "Concepts" section, the Browser uses the database and the codex to find files. Therefore, 
The Browser's configuration actually driven by two files : conf/lucent.py and conf/app_browser.py

### lucent.py

dans le fichier conf/lucent.py, vous pourrez configurer toutes les nomenclatures de votre projet.
pour plus d'informations, vous pouvez consulter la documentation officielle : [Documentation Lucent]https://github.com/tristanlanguebien/lucent

### app_browser.py

ce fichier de configuration permet de définir toute l'inferface du Browser, au sein d'un seul objet AppConfig

config = AppConfig("bigBrowserMainApp")

#### Entities
 La premiere chose est de déclarer les entités auxquelles vous voulez accéder (typiquement, les assets et les shots). ajouter une entité ajoute automatiquement un onglet

asset_entity = Entity(name="asset", collection="assets", filters=["type"])
    config.add_entity(asset_entity)

Le parametre "collection" indique dans quelle collection de votre base de donnée le Browser va aller chercher les Documents. par défaut, BluePepper utilise uniquement les collections "assets" et "shots", mais en fonction de vos besoins, vous pourriez avoir besoin de créer d'autres entités (episodes, levels, etc...) et donc d'autres Collections sur mongodb.

The documents on the database under the provided collection will now appear into the first column in the interface.

#### Tasks
- maintenant, nous pouvons créer des taches dans notre entité. Les taches sont juste une manière de regrouper vos File Kinds pour correspondre aux besoin de vos départements.

asset_modeling_task = Task("modeling")
asset_entity.add_task(asset_modeling_task)

the created tasks will appear in the second column in the interface

#### Kinds
- you can now fill your tasks with Kinds. Kinds are basically a way to access files that match a specific Convention from your project's Codex

kind = Kind(
      name="asset_modeling_workfile_blender",
      label="Workfile (blender)",
      convention=codex.convs.asset_modeling_workfile_blender,
  )
  asset_modeling_task.add_kind(kind)

Kinds will appear in the third column of the interface.

#### Actions
Contextual MenuActions can be added to Documents, Kinds, and Files, allowing you to define which specific actions can be run when you right click on various elements of the interface.

For instance: 

create a new file in conf/scripts. Let's say, print_stuff.py. In this file, create a new function : 

def say_hello():
    print("Hello World")

you can add an action that runs this method using this piece of code : 

action = MenuAction(label="say hello", module="conf.scripts.print_stuff", callable="say_hello")
    asset_entity.add_document_action(action)

When you write click on an asset document, the "say hello" action should appear, and "Hello World" should be written to the console when you click on it.

#### Passing arguments to actions

Saying "Hello World" is nice and all, but what if you need to pass the selected documents/files as arguments ? 

You may use the `kwargs` attribute with these specific keywords, that will be replaced when being passed to your functions : 
- <document> -> each of selected documents
- <documents> -> list of selected documents
- <document_name> -> each of the selected documents' names
- <document_names> -> list of documents' names
- <document_id> -> each of the selected documents' mongodb id
- <document_ids> -> list of documents' mongodb id
- <convention> -> selected Convention object
- <path> -> Each selected path
- <paths> -> List of selected paths
- <browser> -> BrowserWidget object

You may wonder why so many keywords look similar, such as `document` and `documents`. There is in fact a core different between the two. Let's assume you have 10 selected documents: 
- using `document` makes the function being triggered 10 times, one for each document
- using `documents` triggers the function only one time, with the list of documents passed as argument (assuming there is a for loop in the function)
The same logic goes for document_name(s), document_id(s), and path(s)

#### Filtering tasks and actions

What if the rigging task should only appear on characters ? what if an action should only be run on mp4 files ? filters got you covered.

There are two kinds of filters : 
- doc_filter : depends on the document
- path_filter : depends on the path

just create a function that returns True if your condition is met, False otherwise. Let's explore it with examples : 

```python
# Task "Rigging" will only appear if a chr is selected
def is_chr(doc: dict) -> bool:
    if not is_asset(doc):
        return False
    return doc["type"] == "chr"

asset_rigging_task = Task("rigging", doc_filter=is_chr)
asset_entity.add_task(asset_rigging_task)

# Action "Open in VLC" will only appear on mp4 files
def is_mp4(path: Path) -> bool:
    return path.suffix == ".mp4"

action = MenuAction(
    label="Show in VLC",
    module="...",
    callable="...",
    kwargs={"path": "<path>"},
    doc_filter=is_mp4,
)
```

What if i have a character and a prop selected ? The browser got you covered : the menu action will show, but will only be executed on documents that match your filter.

# Controversial takes

BluePepper makes minimal use of complex software architecture, which should be considered as a best practice.
However, a modular architecture can be hard to code with, test, update and deploy.
BluePepper structure is simple : you download the source code, you run the installer, and it works.

Quelques choix sujets à controverse ont été faits dans le but de simplifier l'architecture de BluePepper:

- python configuration files : BluePepper pourrait utiliser des fichiers json/yaml/toml pour les fichiers de configuration ; mais les fichiers python débloquent deux quirks importants : la possibilité de configurer BluePepper de manière plus organique qu'avec de simples valeurs (if/else statements, accès à des variables d'environnement, etc...)
- Un repository = un projet : Vous remarquerez que BluePepper a un seul et unique dossier "conf". C'est volontaire. BluePepper prend ce parti, parce que nous pensons que sa force principale est sa simplicité d'utilisation
- Usage minimal de plugins/entry points : si vous voulez ajouter des features à BluePepper, vous faites un nouveau module python, vous l'importez, ça marche.

Ces choix ont pour objectif:
- De baisser le niveau d'entrée en développement, en particulier pour Technical Directors/tech artists qui n'ont peut etre pas un niveau suffisant pour manipuler des architectures logicielles complexes.
- D'avoir une excellente ergonomie de développement : autocompletion à tous les étages, facilité de configuration.
- Reduction des effets de bords, ce qui permet de déployer BluePepper chez vos collègues sans (trop) avoir peur d'avoir cassé quelque chose
