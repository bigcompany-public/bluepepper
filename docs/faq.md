# FAQ

??? abstract "Installing/Configuring BluePepper"

    ??? question "I need help setting up BluePepper"
        :email: Contact us as `contact@bigcompany.fr`

??? abstract "Developer Questions"
    
    ??? question "What if I have multiple projects?"

        Our experience shows how hard it can be to manage multiple projects that use different workflows and DCCs, which leads to edge cases and ever-growing technical debt. This leads us to believe it is wiser to have one pipeline per project.

        If you really need to work on multiple projects that share the "same" pipeline, create another repository or use another branch on which the configuration files will be set differently.

    ??? question "Why is the codebase so monolithic?"

        BluePepper makes minimal use of complex software architecture. While modular architectures are often considered best practice, they can be difficult to code, test, update, and deploy.

        BluePepper's structure is intentionally simple: you download the source code, run the installer, and it works.

        Several design choices were made to keep things lean:

        - **Python Configuration Files**: BluePepper could use JSON, YAML, or TOML for configuration, but Python files unlock two important capabilities: the ability to configure the application more organically (using if/else statements, environment variable access, etc.) rather than being limited to static values.
        - **One Repository = One Project**: BluePepper has a single `conf` folder, and this is intentional. We believe that simplicity is BluePepper's greatest strength.
        - **Minimal Use of Plugins/Entry Points**: If you want to add features to BluePepper, you simply create a new Python module, import it, and it works.

        These choices aim to:

        - Lower the barrier to entry for development, particularly for technical directors and tech artists who may not have extensive experience with complex software architectures
        - Provide excellent development ergonomics: autocompletion at every level, straightforward configuration
        - Reduce side effects, making it safe to deploy BluePepper to your colleagues without undue risk of breaking anything

??? abstract "Misc"

    ??? question "Who developed BluePepper?"

        BluePepper was developed at Big Company. Its main contributors include:
        
        - Tristan Languebien (lead developer)
        - Terry Maire (technical director)
        - Jean-Philippe Pollien (CEO)

    ??? question "Who made the assets of the demo project?"

        The assets used in the demo project were made at Blender Studio for the open source short film "Sprite Fright". For more information, see [Sprite Fright Gallery](https://studio.blender.org/projects/sprite-fright/gallery/)
