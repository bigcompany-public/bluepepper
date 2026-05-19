# Configuring the Naming Conventions

In the file `conf/naming_conventions.py`:memo:, you can configure all the naming conventions for your project.

In brief: Lucent organises everything within a `Codex`, which contains `Conventions` (string templates made up of fields) and `Rules` (which define how fields should behave). For more information, consult the [Lucent documentation](https://github.com/tristanlanguebien/lucent).

`naming_conventions.py`:memo: comes with a few boilerplate examples demonstrating the various features of Lucent, but you can keep things simple. Here is a minimal version of the Codex:

=== "python"
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

!!! warning
    One important note: the Browser's configuration also relies on Conventions. If you remove a Convention that is used by the Browser, BluePepper will not be able to start. Don't worry, this is covered in the next section.

---

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : Configuring The Browser](./dev_browser.md) </div>