from dataclasses import dataclass, field
from typing import List, override

from language.language import Language
from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Java(Language):
    name: str = field(default="java", repr=False)
    solution_file: str = field(default="src/Solver.java", repr=False)

    @override
    def _setup_command(self) -> List[str]:
        return ["./gradlew", "build", "-q"]

    @override
    def _run_command(self, day: Day, _: List[str]) -> List[str]:
        return ["./gradlew", f":{Java.task(day)}:run", "-q"]

    @override
    def template_processing(self, day: Day) -> None:
        f = open("settings.gradle.kts", "a")
        f.write("\n")
        f.write(f'include("{Java.task(day)}")\n')
        f.write(f'project(":{Java.task(day)}").projectDir = file("{day.dir()}")\n')
        f.close()

    @staticmethod
    def task(day: Day) -> str:
        return f"{day.year}-{day.day}"
