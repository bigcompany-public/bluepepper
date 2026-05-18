# Configuring the Project

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

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : Setting Up The Database](./dev_database.md) </div>