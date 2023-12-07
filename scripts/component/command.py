import subprocess
import time


def execute(command: list[str]) -> float:
    if len(command) == 0:
        return 0.0
    start = time.time()
    result = subprocess.run(command, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(f"Failed due to: {result.stderr.decode()}")
    return time.time() - start
