import subprocess


def execute(command: list[str]) -> str:
    if len(command) == 0:
        return ""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        error_message = result.stderr.decode()
        print(error_message)
        exit(1)
    else:
        return result.stdout.decode()
