# Writing Your First Script

This section will demonstrate how to use the `Database` and the `Codex`. In this example, we will write a script that looks for the last version of an asset workfile, and copy it to a delivery folder (we will be using documents and naming conventions from the demo project, feel free to adjust it to your needs).

!!! tip
    Before going any further, remember to initialize the terminal properly, as specified in [this section](dev_environment/#running-a-script)

    === "powershell"
        ```powershell
        & ./venvs/core_3.11.12/Scripts/python.exe ./main.py --shell
        ```

## Writing The Script Step By Step

### Laying the foundations

Create a new python file `conf/scripts/my_first_script.py` :memo: with a placeholder `main()` function.

=== "Python"
    ```python
    """
    This script is designed to copy the last version of the modeling workfile to a delivery folder
    """

    import sys

    def main(document_id):
        print(f"Processing document ID: {document_id}")

    if __name__ == "__main__":
        main(sys.argv[1])
    ```

??? question "What is `sys.argv` ?"
    `sys.argv` returns the list of arguments provided to python. Index 0 is the path of the script, and index 1 will be the argument provided along the script.

??? question "What is `if __name__ == "__main__"` ?"
    This line of code basically means "if this python file is executed as a script". This prevents the `main()` function from triggering if this python file is imported somewhere else.

You can now run your python script using this command:

=== "powershell"
    ```powershell
    & ./venvs/core_3.11.12/Scripts/python.exe ./conf/scripts/my_first_script.py "paste_document_id_here"

    >>> Processing document ID: 69ea2309a43cd5d382c0801b
    ```

??? question "How to get a document ID?"
    A document's ID can conviniently be copied directly from the Browser

    ![copy_document_id](img/copy_document_id.png)


### Querying The Database

Having a document's ID is nice, but there is not much we ca do with it as-is. Hopefully, the database provides a function to find the document using its ID.

=== "Python"
    ```python
    from bluepepper.core import database

    def main(document_id):
        document = database.get_asset_document_by_id(document_id)
        print(f"Processing document: {document}")
    
    # >>> Processing document: {'_id': '69ea2309a43cd5d382c0801b', 'type': 'chr', 'asset': 'elderSprite', '_tags': ['categorie', 'sprite']}
    ```

### Finding Paths

BluePepper's Codex has functions to find files that match a specific naming convention. In our case, the `get_last_path()` function will fit our needs.

=== "Python"
    ```python
    from bluepepper.core import codex
    
    path = codex.convs.asset_modeling_workfile_blender.get_last_path(document)
    print(path)

    # >>> bluepepper_project\assetWorkspace\chr\elderSprite\mdl\blender\elderSprite_mdl_v001_newFile.blend
    ```

??? question "How did the file seach work?"
    The Convention needed the fields `type`, `asset`, `version` and `description`. The `asset` and `type` by using the document as fields, resulting in a search string looking like this: 

        bluepepper_project\assetWorkspace\chr\elderSprite\mdl\blender\elderSprite_mdl_v*_*.blend
    
    Lucent found all matching files, and returned the last one.

### Constructing A Destination Path

Building paths by splitting and mixing parts of an existing path is not worthy of your time. Let's use the Codex instead.

Add a new Convention to the Codex in `conf/naming_conventions.py` :memo:

=== "Python"
    ```python
    class BluePepperConventions(Conventions):
        ...
        modeling_delivery = Convention("{@project_root}/delivery/{asset}_{task}_v{version}_{description}.{extension}")
    ```

And use this new Convention in our script. We will use the `transmute()` function, to transform a path into another path.

=== "Python"
    ```python
    destination = codex.transmute(path, target_convention=codex.convs.modeling_delivery)
    print(destination)

    # >>> bluepepper_project/delivery/elderSprite_mdl_v001_newFile.blend
    ```

??? question "How did the transmutation work?"
    Lucent extracted the fields from the original path, deducing their value:

    - `asset` = `elderSprite`
    - `type` = `chr`
    - `task` = `mdl`
    - `dcc` = `blender`
    - `version` = `001`
    - `description` = `newFile`
    - `extension` = `blend`

    and used these values to fill the fields of another Convention.

    The `transmute()` function is a shorthand, but you can achieve the same result by parsing the original path and formatting a new one using another Convention.

    === "Python"
        ```python
        fields = codex.convs.asset_modeling_workfile_blender.parse(path)
        destination = codex.convs.modeling_delivery.format(fields)
        ```

### Copying The File

Now that we have the source and the destination, the last step is to proceed to the copy.

=== "Python"
    ```python
    from pathlib import Path
    import shutil

    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(path, destination)
    ```

### Full Code

Here is the full code of our awesome script:

=== "Python"
    ```python
    """
    This script is designed to copy the last version of the modeling workfile to a delivery folder
    """

    import shutil
    import sys
    from pathlib import Path
    from bluepepper.core import codex, database

    def main(document_id):
        document = database.get_asset_document_by_id(document_id)
        path = codex.convs.asset_modeling_workfile_blender.get_last_path(document)
        destination = codex.transmute(path, target_convention=codex.convs.modeling_delivery)
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, destination)

    if __name__ == "__main__":
        main(sys.argv[1])
    ```

As you can see, using the Database in conjunction with the Codex allow file manipulations with very few lines of code.

## Process Assets In Batch

To turn this simple script into something we can actually process as batch, we well follow the steps described in the [Batcher Menu Action Tutorial](./dev_browser/#creating-a-batcher-job-through-a-menuaction). 

Edit the Browser configuration file `conf/app_browser.py` :memo: to add a new 

=== "Python"
    ```python
    from bluepepper.tools.browser.browser_config import BatcherMenuAction

    deliver_modeling_action = BatcherMenuAction(
        label="Deliver Modeling",
        job_name="Deliver Modeling - <document_name>",
        job_description="Copy the workfile into the delivery folder",
        batcher_module="conf.scripts.my_first_script",
        batcher_function="main",
        batcher_kwargs={"document_id": "<document_id>"},
        batcher_notification=True,
        batcher_notification_message="<document_name> - Delivery Done",
        qta_icon="mdi.truck-delivery",
    )

    asset_entity.add_document_action(deliver_modeling_action)
    ```

The contextural action is now available, and the Batch works wonders.

![first_script_action](img/first_script_action.png)
![first_script_batcher](img/first_script_batcher.png)


## Process Files In Batch

For demonstration purposes, we performed document queries and file discovery to get you aquainted with the Database and the Codex, but the Browser can already do most of the heavy lifting.

Our script can be adjusted to take a path as argument instead of a document ID.

=== "Python"
    ```python
    import shutil
    import sys
    from pathlib import Path
    from bluepepper.core import codex

    def main(path):
        destination = codex.transmute(path, target_convention=codex.convs.modeling_delivery)
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, destination)
    ```

And the BatcherMenuAction can be adjusted to be triggered with files instead of documents.

=== "Python"
    ```python
    deliver_modeling_action = BatcherMenuAction(
        label="Deliver Modeling",
        job_name="Deliver Modeling - <document_name>",
        job_description="Copy the workfile into the delivery folder",
        batcher_module="conf.scripts.my_first_script",
        batcher_function="main",
        batcher_kwargs={"path": "<path>"},
        batcher_notification=True,
        batcher_notification_message="<document_name> - Delivery Done",
        qta_icon="mdi.truck-delivery",
    )

    modeling_workfile_kind.add_file_action(deliver_modeling_action)
    ```

The Action can now be triggered on files, and the result will be the same.

![first_script_action_files](img/first_script_action_files.png)
![first_script_batcher](img/first_script_batcher.png)


---

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : Embedded FastAPI Server](./dev_fastapi.md) </div>