import subprocess

from bluepepper.core import root_dir
from install.install import BluePepperInstaller


def open():
    """Opens powershell with the BluePepper virtual environment activated"""
    installer = BluePepperInstaller()
    activate_script = installer.core_python_exe.parent / "activate.ps1"
    command = [
        "powershell",
        "-Command",
        f"Start-Process powershell -ArgumentList '-NoExit', '-File', '{activate_script.as_posix()}'",
    ]
    subprocess.Popen(
        command,
        cwd=root_dir.as_posix(),
    )


if __name__ == "__main__":
    open()
