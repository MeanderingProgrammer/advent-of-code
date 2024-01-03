import subprocess


def execute(command: list[str]) -> None:
    if len(command) == 0:
        return None
    result = subprocess.run(command, stderr=subprocess.PIPE)
    if result.returncode != 0:
        error_message = result.stderr.decode()
        print(error_message)
        exit(1)
    return None
