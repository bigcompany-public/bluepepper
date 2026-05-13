# Setting Up a Development Environment

## Forking and Cloning

- Fork the repository to your personal GitHub page (for example, `bluepepper_myProject`). This will make it easier to edit the configuration and deploy it to your team later.
- Clone the repository.

    ```
    git clone https://github.com/my-account/bluepepper_myproject.git
    ```

## Installation

- Run `install_dev.bat`.
- You can now open the app using the newly created BluePepper shortcut, but let's do some configuration first.


## Configuring the Project

Edit the file `conf/project.py`:memo: to match your project's needs:

=== "python"
    ```python
    class ProjectSettings:
        project_name: str = "MyIncredibleProject"
        project_code: str = "proj"
        width: int = 1920
        height: int = 1080
        fps: float = 25.0
        start_frame: int = 101
        production_trackers: list[str] = []
    ```