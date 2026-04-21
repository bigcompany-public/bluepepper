import os
from pathlib import Path

from lucent import Codex, Convention, Conventions, Rule, Rules

_project_root = os.environ.get("BLUEPEPPER_PROJECT_ROOT")
if _project_root:
    PROJECT_ROOT = Path(_project_root)
else:
    root_dir = Path(os.environ["BLUEPEPPER_ROOT"])
    PROJECT_ROOT = root_dir.parent.joinpath(f"{root_dir.name}_project")


class BluePepperRules(Rules):
    default = Rule(r"[a-zA-Z0-9]+")
    extension = Rule(r"[a-zA-Z0-9]+", examples=["mp3", "png", "mov"])
    project = Rule(r"[a-zA-Z]+", examples=["mySuperProject"])
    asset = Rule(r"([a-z]+)([A-Z][a-z]*)*", examples=["peach", "redApple", "philip", "cassie"])
    type = Rule(r"[a-z]+", examples=["prp", "chr", "elem"])
    season = Rule(r"s\d{3}", examples=["s001"])
    episode = Rule(r"ep\d{3}", examples=["ep001"])
    sequence = Rule(r"sq\d{3}", examples=["sq001"])
    shot = Rule(r"sh\d{4}[A-Z]?", examples=["sh0010", "sh0010A"])
    version = Rule(r"\d{3}", examples=["001", "002", "003"])
    frame = Rule(r"\d{4}|#{4}|%04d", examples=["0001", "####", "%04d"])
    dcc = Rule(r"[a-z]+", examples=["maya", "blender", "nuke"])
    description = Rule(r"[a-zA-Z0-9]+", examples=["doingStuff", "startWork", "fixingSomething2"])
    tag = Rule(r"[a-zA-Z0-9]+", examples=["important", "yolo"])


class BluePepperConventions(Conventions):
    # Project
    project_root = Convention(PROJECT_ROOT.as_posix())

    # Configuration for entity creation
    asset_identifier = Convention("{asset}")
    asset_fields = Convention("{type}_{asset}")
    shot_identifier = Convention("{season}_{episode}_{shot}")
    shot_fields = Convention("{season}_{episode}_{sequence}_{shot}")
    episode_identifier = Convention("{season}_{episode}")
    episode_fields = Convention("{season}_{episode}")

    # Aquarium
    aquarium_asset = Convention("assets/{type}/{asset}")
    aquarium_shot = Convention("shots/{season}/{episode}/{shot}")

    # Assets
    asset_work_dir = Convention("{@project_root}/assetWorkspace/{type}/{asset}/{task}/{dcc}")
    asset_workfile = Convention("{@asset_work_dir}/{asset}_{task}_v{version}_{description}.{extension}")
    asset_modeling_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "mdl"})
    asset_surfacing_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "sur"})
    asset_texturing_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "tex"})
    asset_rigging_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "rig"})
    asset_grooming_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "gro"})
    asset_fx_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "afx"})
    asset_anim_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "ani"})
    asset_assembly_workfile = Convention("{@asset_workfile}", fixed_fields={"task": "asb"})

    # Asset maya
    asset_modeling_workfile_maya = Convention(
        "{@asset_modeling_workfile}", fixed_fields={"dcc": "maya", "extension": "ma"}
    )

    # Shots
    shot_work_dir = Convention("{@project_root}/shots/{season}/{episode}/{shot}/{task}/work")
    shot_workfile = Convention("{@shot_work_dir}/{@shot_identifier}_{task}_v{version}_{description}.{extension}")
    shot_layout_workfile = Convention(
        "{@shot_workfile}",
        fixed_fields={"task": "lay", "dcc": "maya", "extension": "ma"},
    )

    # Asset blender
    asset_modeling_workfile_blender = Convention(
        "{@asset_modeling_workfile}",
        fixed_fields={"dcc": "blender", "extension": "blend"},
    )
    asset_surfacing_workfile_blender = Convention(
        "{@asset_surfacing_workfile}",
        fixed_fields={"dcc": "blender", "extension": "blend"},
    )
    asset_texturing_workfile_blender = Convention(
        "{@asset_texturing_workfile}",
        fixed_fields={"dcc": "blender", "extension": "blend"},
    )
    asset_rigging_workfile_blender = Convention(
        "{@asset_rigging_workfile}",
        fixed_fields={"dcc": "blender", "extension": "blend"},
    )
    asset_grooming_workfile_blender = Convention(
        "{@asset_grooming_workfile}",
        fixed_fields={"dcc": "blender", "extension": "blend"},
    )
    asset_fx_workfile_blender = Convention(
        "{@asset_fx_workfile}", fixed_fields={"dcc": "blender", "extension": "blend"}
    )
    asset_assembly_workfile_blender = Convention(
        "{@asset_assembly_workfile}",
        fixed_fields={"dcc": "blender", "extension": "blend"},
    )

    # User directory
    shared_user_dir = Convention("{@project_root}/users/{$USERNAME}")


class BluePepperCodex(Codex):
    convs: BluePepperConventions = BluePepperConventions()
    rules: BluePepperRules = BluePepperRules()


codex = BluePepperCodex()


if __name__ == "__main__":
    # Test your codex here
    print(codex.human_readable)
