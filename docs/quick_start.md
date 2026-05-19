# Quick Start

## Installation

- :package: [Download the source code](https://github.com/bigcompany-public/bluepepper/archive/refs/heads/main.zip).
- Unzip it.

    !!! tip
        When working on a local project, additional folders are created at first launch. You should unzip it into a new folder, for example `myProject`:open_file_folder:

        ![install_folder](img/install_folder.jpg)

- Run `install_dev.bat`:memo:.
- Double-click the newly created BluePepper shortcut.

From here, it is advised to:

??? success "Download the demo project"
    At first launch, if BluePeppers detects the project is empty, you will be prompted if you want to dowload a demo project.

    ![download_project](img/download_project.jpg)

    If you press "Yes", BluePepper will set up a database with a few assets/shots and will download a few blender files
    for you to play with.

    ![demo_project](img/demo_project.jpg)

??? success "Create a few assets/shots manually"
    At first launch, if BluePeppers detects the project is empty, you will be prompted if you want to dowload a demo project.

    Just click `No`, and go to the EntityCreator page to create your own assets/shots

    ![quickstart_entitycreator](img/entitycreator.jpg)

Once this is done, you can play around in the Browser to see what you can do.


## Experimenting With Configuration Files

If you're feeling adventurous, you can explore the files in the `conf`:open_file_folder: folder and get a sneak peek at the inner workings of BluePepper.

??? question "I don't know where to start"
    Don't worry if you feel a bit lost with configuration files. Everything is explained in details in the [TD/Dev Documentation](./dev_core_concepts).

    To start things off, you may take a look at `project.py` :memo:, `naming_conventions.py` :memo: and `app_browser.py` :memo:

![conf_files](img/conf_files.jpg)

---

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : Video Tutorials](./video_tutorials.md) </div>
