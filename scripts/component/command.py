import subprocess


def execute(command: list[str]) -> str:
    if len(command) == 0:
        return ""
    result = subprocess.run(command, capture_output=True, text=True)
    error = result.stderr.strip()
    if len(error) != 0:
        print(error)
    output = result.stdout.strip()
    if len(output) != 0:
        print(output)
    if result.returncode != 0:
        exit(1)
    return output
