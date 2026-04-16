
import os
import argparse
import subprocess
from pathlib import Path


class VsCodeLauncher():
    def __init__(self, path: Path = None):
        self.path = Path(path) if path else None

    @property
    def executable(self) -> Path:
        executables = [
            Path(fr"C:\Users\{os.environ['USERNAME']}\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        ]
        for executable in executables:
            if executable.exists():
                return executable
        raise FileNotFoundError("No VSCode executable was found")

    def open(self):
        command = [self.executable.as_posix()]
        if self.path:
            command.append(self.path.as_posix())
        subprocess.Popen(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=False)
    args = parser.parse_args()
    app = VsCodeLauncher(args.path)
    app.open()
