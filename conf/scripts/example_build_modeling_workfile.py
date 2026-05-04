import logging
import shutil
from pathlib import Path

from bluepepper.core import codex, init_logging


def main(document: dict):
    init_logging("blenderBuild")

    # Get blender file to copy
    source = codex.convs.empty_blender_file.get_paths()[0]

    # Get location to copy it to
    fields = document.copy()
    fields["version"] = "001"
    fields["description"] = "newFile"
    destination = Path(codex.convs.asset_modeling_workfile_blender.format(fields))

    # Copy
    if destination.exists():
        raise FileExistsError(f"The file already exists : {destination}")
    logging.info(f"Copying {source.name} to {destination}")
    destination.parent.mkdir(exist_ok=True, parents=True)
    shutil.copy(source, destination)
