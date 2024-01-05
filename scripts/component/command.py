import subprocess


def execute(command: list[str]) -> str:
    if len(command) == 0:
        return ""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = result.stderr.decode()
    if len(error) != 0:
        print(error)
    output = result.stdout.decode()
    if len(output) != 0:
        print(output)
    if result.returncode != 0:
        exit(1)
    return output
