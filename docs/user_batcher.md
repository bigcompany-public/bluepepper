# Batcher

The Batcher is BluePepper's background job manager. Jobs are usually submitted to the Batcher using [Browser Actions](./user_browser/#actions)

![!batcher](img/batcher.jpg)


## Managing Jobs

When submitted, all jobs get the `Waiting` status and are executed in priority order. If jobs share the same priority, the manager runs them in submission order (first-in, first-out).

Here are the actions you can perform on jobs:

![!batcher_buttons](img/batcher_buttons.jpg)

- :one: Change job priority
- :two: Start job
- :three: Stop job
- :four: Restart job
- :five: Delete job

??? question "Sometimes, clicking "Start" does not start my job"
    The `Start Job` button sets a job's status to `Waiting` if its current status was `Error` or `Terminated`. The job manager will execute it when its turn comes: jobs with higher priority run first.

??? question "What is the difference between Start and Restart?"
    The `Start Job` button ignores jobs that are already running. The `Restart Job` button will terminate running jobs before setting their status to `Waiting`.

### Job Selection

Every button press (priority change, start, stop...) affects all selected jobs.

The Job List has an extended selection mode; the following shortcuts are available:

!!! tip ""
    - `Ctrl` + `click` -> additive selection
    - `Shift` + `click` -> contiguous selection
    - `Ctrl` + `A` -> Select all
    - `Shift` + `left/right arrow` -> Extend selection up/down
    - `Ctrl` + `Space` -> Unselect last selected item

### Additional Shortcuts

!!! tip ""
    - `Suppr` -> Terminate and delete selected jobs


## Options

The Options panel can be expanded or collapsed by clicking the Options caret.

![!batcher_options_caret](img/batcher_options_caret.jpg)

### Maximum Threads

Total number of jobs allowed to run simultaneously. Reducing it to zero prevents any new job from starting.

### Sorting

Jobs can be sorted by:

- date
- name
- priority
- status

You may sort them in ascending or descending order.

### Automatically Start Jobs

Toggle whether the Job Manager should start jobs as soon as slots are available. If unchecked, new jobs will not start even if slots are available (see [Maximum Threads](./user_batcher/#maximum-threads)).

### Delete Finished Jobs

If checked, jobs will be removed when done. By default this option is unchecked, so you have the opportunity to read logs of finished jobs.

### Mute Notifications

When executing hundreds of jobs, notifications can be overwhelming. The Batcher lets you control `Success` and `Error` notifications.

Adjust these settings to show only the notifications you need.

## Process Files In Batch

!!! tip "For advanced users only"

BluePepper provides a built-in way to process files in batch by submitting a job to the Batcher for each selected file.

For demonstration purposes, create a new script `conf/scripts/my_script.py` :memo::

=== "python"
    ```python
    import sys

    def do_stuff(path):
        print(f"Doing stuff on {path}")

    if __name__ == "__main__":
        # The selected file that is passed as an argument by the Browser
        path = sys.argv[1]
        do_stuff(path)
    ```

Now, right-click the file(s) to process, run the action `Execute Python Script`, and drop your script on the dialog.

![!batcher_python_script_file](img/batcher_python_script_file.png)
![!batcher_python_script_drop](img/batcher_python_script_drop.png)

A job should appear in the Batcher. You can see the `do_stuff` function ran and printed the file's path.

![!batcher_python_script_file_result](img/batcher_python_script_file_result.png)

You can now select as many files as you wish and batch any script you like.

![!batcher_python_script_files](img/batcher_python_script_files.png)
![!batcher_python_script_files_result](img/batcher_python_script_files_result.png)

!!! warning
    Batch operations can be powerful but also dangerous: you may break many files quickly. Add backup logic if your script removes or overwrites files.

### About Documents

You can also send jobs to the Batcher from a document selection.

![!batcher_python_script_document](img/batcher_python_script_document.png)

In this case, the document id is passed as an argument to the script. You will need to query the database in your script to recover the document. Here is an updated example that demonstrates this.

=== "python"
    ```python
    import sys
    from bluepepper.core import database

    def do_stuff(document_id):
        document = database.get_asset_document_by_id(document_id)
        print("Here is the document from the database:")
        print(document)
        print(f"Doing stuff on {document['asset']}")

    if __name__ == "__main__":
        document_id = sys.argv[1]
        do_stuff(document_id)
    ```

As with files, the script is executed for each selected document.

![!batcher_python_script_document_result](img/batcher_python_script_document_result.png)

---

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : EntityCreator](./user_entitycreator.md) </div>