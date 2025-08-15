from dataclasses import dataclass

from pojo.day import Day


@dataclass(frozen=True)
class Java:
    name: str = "java"
    file: str = "src/Solver.java"
    cmd: str = "gradle"

    def test(self) -> list[str]:
        return ["./gradlew", "test"]

    def build(self) -> list[list[str]]:
        return [["./gradlew", "build", "-q"]]

    def run(self, day: Day, args: list[str]) -> list[str]:
        arg = " ".join(args)
        args = [] if len(args) == 0 else [f'--args="{arg}"']
        return ["./gradlew", f":{Java.task(day)}:run", "-q"] + args

    def setup(self, day: Day) -> None:
        f = open("settings.gradle.kts", "a")
        f.write("\n")
        f.write(f'include("{Java.task(day)}")\n')
        f.write(f'project(":{Java.task(day)}").projectDir = file("{day.dir()}")\n')
        f.close()

    @staticmethod
    def task(day: Day) -> str:
        return f"{day.year}-{day.day}"
