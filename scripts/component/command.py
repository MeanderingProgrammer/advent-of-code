import subprocess
from typing import Optional


def execute(command: list[str]) -> Optional[str]:
    if len(command) == 0:
        return None
    result = subprocess.run(command, stderr=subprocess.PIPE)
    if result.returncode != 0:
        return result.stderr.decode()
    return None
