import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
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
    save_slow: bool

    def run(self) -> None:
        start = time.time()
        runtimes = self.__get_runtimes()
        overall_runtime = time.time() - start

        displayer = Displayer()
        displayer.display("ALL", runtimes)
        slow = list(filter(lambda runtime: runtime.runtime > self.slow, runtimes))
        displayer.display("SLOW", slow)

        print(f"Overall runtime: {overall_runtime:.3f} seconds")

        if self.save_slow:
            with open("slow.json", "w") as f:
                save_value = [runtime.as_dict() for runtime in slow]
                f.write(json.dumps(save_value))

    def __get_runtimes(self) -> List[RuntimeInfo]:
        runtimes = []
        for day in self.days:
            os.chdir(f"{day.year}/{day.day}")
            runtimes.extend(self.__run_day(day))
            os.chdir("../..")
        return runtimes

    def __run_day(self, day: Day) -> List[RuntimeInfo]:
        runtimes = []
        for language in self.__languages():
            runtime = self.__run_language(language, day)
            runtimes.append(runtime)
        return runtimes

    def __languages(self) -> List[Language]:
        return [
            language
            for language in self.languages
            if Path(language.solution_file).is_file()
        ]

    def __run_language(self, language: Language, day: Day) -> RuntimeInfo:
        print(f"Running year {day.year} day {day.day} with {language.name}")
        language.initial_setup()
        language.compile()
        runtime = language.run(day, self.run_args)
        print(f"Runtime: {runtime:.3f} seconds")
        return RuntimeInfo(day, language.name, runtime)
