# Configuring the Naming Conventions

!!! note
    One important note: the Browser's configuration also relies on Conventions. If you remove a Convention that is used by the Browser, BluePepper will not be able to start. Don't worry, this is covered in the next section.

In the file `conf/naming_conventions.py`:memo:, you can configure all the naming conventions for your project.

In brief: Lucent organises everything within a `Codex`, which contains `Conventions` (string templates made up of fields) and `Rules` (which define how fields should behave). For more information, consult the [Lucent documentation](https://github.com/tristanlanguebien/lucent).

`naming_conventions.py`:memo: comes with a few boilerplate examples demonstrating the various features of Lucent, but let's build our own `Codex` from scratch.

## Defining Rules

First, we shall define what are the authorized characters for the various fields. Here are a few general guidelines:

!!! success "Recommended"
    The default value we recommend is letters and digits, mainly to exclude special characters and spaces, which are known to cause issues in paths and across multiple DCCs.

!!! warning "Not Recommended"
    Avoid characters universally understood as separators like `_`, `-` or `.`: you will risk making fields detection quite complicated.

    ??? question "What if I need separators within a field?"
        We recommend using:

        - camelcase (`exampleOfMultiPartField`)
            or
        - kebabcase (`example-of-multi-part-field`)
        
        in conjunction with being very strict about what are considered field separators (for instance, having `_` as your universal separator).

### Default Rule

To begin with, we will set the (mandatory) `default` rule, that will apply to all fields unless specified otherwise.

=== "python"
    ```python
    # Import all objects we will use from lucent
    from lucent import Codex, Convention, Conventions, Rule, Rules

    class BluePepperRules(Rules):
        default = Rule(r"[a-zA-Z0-9]+")
    ```

### Extra Rules

Now, you can add more Rules to enforce on specific fields. To help the end user, you can provide examples that will appear in tooltips and error messages.

=== "python"
    ```python
    class BluePepperRules(Rules):
        default = Rule(r"[a-zA-Z0-9]+")
        asset = Rule(r"([a-z]+)([A-Z][a-z]*)*", examples=["peach", "redApple", "philip", "cassie"])
        type = Rule(r"[a-z]+", examples=["prp", "chr", "elem"])
        sequence = Rule(r"sq\d{3}", examples=["sq001"])
        shot = Rule(r"sh\d{4}[A-Z]?", examples=["sh0010", "sh0010A"])
        version = Rule(r"\d{3}", examples=["001", "002", "003"])
    ```

### Cheat Sheet

- lower-case letters only : `[a-z]+`
- lower-case and upper-case letters only : `[a-zA-Z]+`
- lower-case/upper-case letters + digits only : `[a-zA-Z0-9]+`
- camel-case : `([a-z]+)([A-Z][a-z]*)*`
- kebab-case : `([a-z]+)(-[a-z]*)*`

## Defining Conventions

Now, let's define the Conventions (on which the Rules we just made will apply).

### File Path Conventions

=== "python"
    ```python
    class BluePepperConventions(Conventions):
        project_root = Convention("D:/projects/my_project")
        asset_work_dir = Convention("{@project_root}/assetWorkspace/{type}/{asset}")
    ```

- The `project_root` Convention is simple and has no moving parts.
- `asset_work_dir`, on the other hand, references `project_root` using the `{@convention}` syntax, and uses two fields using the `{field}` syntax

---

Let's add a few more Conventions, shall we?

=== "python"
    ```python
    asset_workfile = Convention("{@asset_work_dir}/{asset}_{task}_v{version}.{extension}")
    asset_modeling_workfile = Convention(
        "{@asset_workfile}",
        fixed_fields={"task": "mdl", "extension" : "blend"}
    )
    ```

The Convention `asset_modeling_workfile` introduces a new concept: fixed fields. In this case, `asset_modeling_workfile` is a variant of `asset_workfile`, where the values of `task` and `extension` are enforced.

### Entity Configuration Conventions

The Codex is also used to configure entities such as assets and shots. After all, we need to create documents on the database with fields that respect the Rules we defined earlier.

=== "python"
    ```python
    asset_fields = Convention("{type}_{asset}")
    asset_identifier = Convention("{asset}")
    shot_fields = Convention("{sequence}_{shot}")
    shot_identifier = Convention("{shot}")
    ```

- the `asset_fields` and `shot_fields` Conventions configure the fields that are mandatory to create an asset or a shot
- the `asset_identifier` and `shot_identifier` are Conventions for how BluePepper should "represent" your documents. This example is simple, but imagine an episodic show with multiple seasons and episodes, each of which have a shot named "sh0001". In that case, the proper way of representing a shot won't be `sh0001`, but `s001_ep001_sh0001`

### Wrapping Up The Codex

Finally, we can bind the Rules and the Conventions into a single Codex.

=== "python"
    ```python
    class BluePepperCodex(Codex):
        convs: BluePepperConventions = BluePepperConventions()
        rules: BluePepperRules = BluePepperRules()

    codex = BluePepperCodex()
    ```

!!! tip
    You may have noticed the redundant typing annotations. This is on purpose: if you don't, the autocompletion will not work.

From now on, the Codex can be accessed in all parts of BluePepper, including your python scripts.

---

### Full Code

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
        # Paths
        project_root = Convention("D:/projects/my_project")
        asset_work_dir = Convention("{@project_root}/assetWorkspace/{type}/{asset}")
        asset_workfile = Convention("{@asset_work_dir}/{asset}_{task}_v{version}.{extension}")
        asset_modeling_workfile = Convention(
            "{@asset_workfile}",
            fixed_fields={"task": "mdl", "extension" : "blend"}
        )

        # Documents Configuration
        asset_fields = Convention("{type}_{asset}")
        asset_identifier = Convention("{asset}")
        shot_fields = Convention("{sequence}_{shot}")
        shot_identifier = Convention("{shot}")

    class BluePepperCodex(Codex):
        convs: BluePepperConventions = BluePepperConventions()
        rules: BluePepperRules = BluePepperRules()

    codex = BluePepperCodex()
    ```

!!! info ""
    <a href="Next Section"> <div style="text-align: right; font-weight: bold"> [Next Section : Configuring The Browser](./dev_browser.md) </div>