import subprocess


def execute(command: list[str]) -> str:
    if len(command) == 0:
        return ""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode()
    if result.returncode != 0:
        print(output)
        print(result.stderr.decode())
        exit(1)
    return output
