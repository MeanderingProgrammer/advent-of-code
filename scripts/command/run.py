import json
import re
import time
from dataclasses import dataclass
from typing import override

from command.command import Command
from component.command import execute
from component.display_runtimes import Displayer
from component.language_strategy import LanguageStrategy
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class LanguageRunner:
    day: Day
    name: str
    command: list[str]

    def as_dict(self) -> dict:
        return dict(
            year=self.day.year,
            day=self.day.day,
            name=self.name,
            command=" ".join(self.command),
        )

    def execute(self) -> RuntimeInfo:
        print(f"Running year {self.day.year} day {self.day.day} with {self.name}")
        result = execute(self.command)
        runtime = LanguageRunner.__parse_runtime_seconds(result)
        return RuntimeInfo(self.day, self.name, runtime)

    @staticmethod
    def __parse_runtime_seconds(result: str) -> float:
        matches: list[str] = re.findall(r".*Runtime \(ns\): (\d*)", result)
        assert len(matches) == 1, "Could not find runtime in output"
        runtime_ns = float(matches[0])
        return runtime_ns / 1_000_000_000


@dataclass(frozen=True)
class Runner(Command):
    days: list[Day]
    language_strategy: LanguageStrategy
    slow: int
    run_args: list[str]
    save: bool

    @override
    def info(self) -> dict:
        return dict(
            executions=[runner.as_dict() for runner in self.__language_runners()],
            slow=self.slow,
            save=self.save,
        )

    @override
    def run(self) -> None:
        start = time.time()
        runtimes = [runner.execute() for runner in self.__language_runners()]
        overall_runtime = time.time() - start

        displayer = Displayer()
        displayer.display("ALL", runtimes)
        self.__save("all", runtimes)

        slow = list(filter(lambda runtime: runtime.runtime > self.slow, runtimes))
        displayer.display("SLOW", slow)
        self.__save("slow", slow)

        print(f"Overall runtime: {overall_runtime:.3f} seconds")

    def __save(self, name: str, runtimes: list[RuntimeInfo]) -> None:
        if not self.save:
            return
        with open(f"{name}.json", "w") as f:
            value = [runtime.as_dict() for runtime in runtimes]
            f.write(json.dumps(value))

    def __language_runners(self) -> list[LanguageRunner]:
        result: list[LanguageRunner] = []
        for day in self.days:
            for language in self.language_strategy.get(day):
                runner = LanguageRunner(
                    day=day,
                    name=language.name,
                    command=language.run_command(day, self.run_args),
                )
                result.append(runner)
        return result
