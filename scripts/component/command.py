import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

env = os.environ.copy()
env["FORCE_COLOR"] = "1"
env["CLICOLOR_FORCE"] = "1"


@dataclass(frozen=True)
class Executor:
    output: bool = True

    def call(self, args: list[str], cwd: Path | None = None) -> None:
        subprocess.run(args, cwd=cwd, check=True)

    def run(self, args: list[str]) -> str:
        if len(args) == 0:
            return ""

        result = subprocess.run(args, env=env, capture_output=True, text=True)
        output = self.tee(result.stdout)
        self.tee(result.stderr)
        if result.returncode != 0:
            exit(1)
        return output

    def tee(self, value: str) -> str:
        value = value.strip()
        if self.output and len(value) > 0:
            print(value)
        return value
