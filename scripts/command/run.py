import json
import subprocess
import time
from dataclasses import dataclass
from typing import List

from component.display_runtimes import Displayer
from language.language import Language
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class Runner:
    days: List[Day]
    languages: List[Language]
    slow: int
    run_args: List[str]
    save: bool

    def run(self) -> None:
        start = time.time()
        runtimes = self.__get_runtimes()
        overall_runtime = time.time() - start

        displayer = Displayer()
        displayer.display("ALL", runtimes)
        self.__save("all", runtimes)

        slow = list(filter(lambda runtime: runtime.runtime > self.slow, runtimes))
        displayer.display("SLOW", slow)
        self.__save("slow", slow)

        print(f"Overall runtime: {overall_runtime:.3f} seconds")

    def __get_runtimes(self) -> List[RuntimeInfo]:
        runtimes = []
        for day in self.days:
            runtimes.extend(self.__run_day(day))
        return runtimes

    def __run_day(self, day: Day) -> List[RuntimeInfo]:
        runtimes = []
        for language in self.__languages(day):
            runtime = self.__run_language(language, day)
            runtimes.append(runtime)
        return runtimes

    def __languages(self, day: Day) -> List[Language]:
        return [
            language
            for language in self.languages
            if day.dir().joinpath(language.solution_file).is_file()
        ]

    def __run_language(self, language: Language, day: Day) -> RuntimeInfo:
        print(f"Running year {day.year} day {day.day} with {language.name}")
        Runner.__execute(language.setup_command())
        runtime = Runner.__execute(language.run_command(day, self.run_args))
        print(f"Runtime: {runtime:.3f} seconds")
        return RuntimeInfo(day, language.name, runtime)

    @staticmethod
    def __execute(command: List[str]) -> float:
        if len(command) == 0:
            return 0
        start = time.time()
        result = subprocess.run(command, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"Failed due to: {result.stderr.decode()}")
        return time.time() - start

    def __save(self, name: str, runtimes: List[RuntimeInfo]) -> None:
        if not self.save:
            return
        with open(f"{name}.json", "w") as f:
            value = [runtime.as_dict() for runtime in runtimes]
            f.write(json.dumps(value))
