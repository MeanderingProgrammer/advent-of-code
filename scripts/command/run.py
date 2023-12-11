import json
import time
from dataclasses import dataclass

from component.command import execute
from component.display_runtimes import Displayer
from component.language_strategy import LanguageStrategy
from language.language import Language
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class Runner:
    days: list[Day]
    language_strategy: LanguageStrategy
    slow: int
    run_args: list[str]
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

    def __get_runtimes(self) -> list[RuntimeInfo]:
        runtimes = []
        for day in self.days:
            runtimes.extend(self.__run_day(day))
        return runtimes

    def __run_day(self, day: Day) -> list[RuntimeInfo]:
        runtimes = []
        for language in self.language_strategy.get(day):
            runtime = self.__run_language(language, day)
            runtimes.append(runtime)
        return runtimes

    def __run_language(self, language: Language, day: Day) -> RuntimeInfo:
        print(f"Running year {day.year} day {day.day} with {language.name}")
        start = time.time()
        error_message = execute(language.run_command(day, self.run_args))
        if error_message is not None:
            print(error_message)
            exit(1)
        runtime = time.time() - start
        print(f"Runtime: {runtime:.3f} seconds")
        return RuntimeInfo(day, language.name, runtime)

    def __save(self, name: str, runtimes: list[RuntimeInfo]) -> None:
        if not self.save:
            return
        with open(f"{name}.json", "w") as f:
            value = [runtime.as_dict() for runtime in runtimes]
            f.write(json.dumps(value))
