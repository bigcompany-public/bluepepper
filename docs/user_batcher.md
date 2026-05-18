# Batcher

The Batcher is BluePepper's background job manager. Jobs are usually submitted to the Batcher using [Browser Actions](./user_browser/#actions)

![!batcher](img/batcher.jpg)


## Managing Jobs

When submitted, all jobs shall have the `Waiting` status, then are executed in order of priority. If some jobs share the same priority, the manager will run jobs sorted by submission time (first-in, first-out)

Here are the actions you can perform on jobs:

![!batcher_buttons](img/batcher_buttons.jpg)

- :one: Change job priority
- :two: Start job
- :three: Stop job
- :four: Retart job
- :five: Delete job

??? question "Sometimes, clicking "Start" does not start my job"
    The `Start Job` button actually sets the Job's status to `Waiting` in case it's current status was `Error` or `Terminated`, but the job manager will only execute it when the time comes : jobs that have a higher priority will be executed first.

??? question "What is the difference between Start and Restart?"
    In contrast with the `Start Job` button which ignores jobs that are already running, the `Restart Job` button will terminate running jobs before setting their status to `Waiting`

### Job Selection

Every button pressed (priority change, start, stop...) affects all selected jobs.

The Job List has an extended selection mode, so various shortcuts are available:

- `Ctrl` + `click` -> additive selection 
- `Shift` + `click` -> contiguous selection
- `Ctrl` + `A` -> Select all
- `Shift` + `left/right arrow` -> Extend selection up/down
- `Ctrl` + `Space` -> Unselect last selected item

### Additional Shortcuts

- `Suppr` -> Terminate and delete selected jobs  


## Options

The Options panel can be expanded/collapsed by clicking on the Options caret.

![!batcher_options_caret](img/batcher_options_caret.jpg)

### Maximum Threads

Total number of jobs allowed to run simultaneously. Reducing it to zero will prevent any new job from starting.

### Sorting

Jobs can be sorted by:

- date
- name
- priority
- status

You may sort them in ascending or descending order

### Automatically Start Jobs

Tells the Job Manager if jobs should start as soon as possible. If unchecked, new jobs will not start, event if slots are available (see [Maximum Threads](./user_batcher/#maximum-threads))

### Delete Finished Jobs

If checked, the Jobs will be removed when done. By default, this option is unchecked, to give you the opportunity to read logs of finished Jobs.

### Mute Notifications

Being flooded with notifications when executing hundreds of jobs can be overwhelming: to mitigate this, the Batcher gives you control over `Success` and `Error` notifications. 

Feel free to adjust these settings to show exactly the notifications you actually need.

---

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : EntityCreator](./user_entitycreator.md) </div>