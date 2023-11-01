import os
from typing import List, override

from language.language import Language
from pojo.day import Day


class Java(Language):
    @property
    @override
    def name(self) -> str:
        return "java"

    @property
    @override
    def solution_file(self) -> str:
        return "src/Solver.java"

    @override
    def _run_setup(self) -> None:
        os.system("./gradlew build -q")

    @override
    def _get_run_command(self, day: Day, _: List[str]) -> List[str]:
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
