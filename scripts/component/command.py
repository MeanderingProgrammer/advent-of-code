import os
import subprocess

env = os.environ.copy()
env["FORCE_COLOR"] = "1"
env["CLICOLOR_FORCE"] = "1"


def execute(command: list[str]) -> str:
    if len(command) == 0:
        return ""

    result = subprocess.run(command, env=env, capture_output=True, text=True)
    tee(result.stderr)
    output = tee(result.stdout)
    if result.returncode != 0:
        exit(1)
    return output


def tee(value: str) -> str:
    value = value.strip()
    if len(value) != 0:
        print(value)
    return value
