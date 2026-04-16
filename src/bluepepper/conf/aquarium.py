class AquariumConfig:
    # Connection info
    # WARNING : Do not push sensitive data to the repository, use environment variables or keyring instead
    url: str = "https://mycompany.aquarium.app"
    project: str = "myproject"
    bot_secret: str = ""
    bot_key: str = ""

    # Colors
    asset_color: str = "#fd7b1f"
    shot_color: str = "#ab7df6"

    # Templates
    asset_templates: dict[str, int] = {"_default": 111111111}
    shot_template: int = 222222222
