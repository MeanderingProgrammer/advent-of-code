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
    times: int
    command: list[str]

    def as_dict(self) -> dict:
        return dict(
            year=self.day.year,
            day=self.day.day,
            name=self.name,
            times=self.times,
            command=" ".join(self.command),
        )

    def execute(self) -> RuntimeInfo:
        message = (
            f"Running {self.day.year}/{self.day.day}"
            f" {self.times} times with {self.name}"
        )
        print(message)

        runtimes: list[float] = []
        executions: list[float] = []
        for _ in range(self.times):
            runtime, execution = LanguageRunner.run_command(self.command)
            runtimes.append(runtime)
            executions.append(execution)

        return RuntimeInfo(
            day=self.day,
            language=self.name,
            runtime=sum(runtimes) / self.times,
            execution=sum(executions) / self.times,
        )

    @staticmethod
    def run_command(command: list[str]) -> tuple[float, float]:
        start = time.time_ns()
        result = execute(command)
        execution_ns = float(time.time_ns() - start)
        matches: list[str] = re.findall(r".*Runtime \(ns\): (\d*)", result)
        assert len(matches) == 1, "Could not find runtime in output"
        runtime_ns = float(matches[0])
        return (runtime_ns / 1_000_000, execution_ns / 1_000_000)


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
            executions=[runner.as_dict() for runner in self.runners()],
            slow=self.slow,
            save=self.save,
        )

    @override
    def run(self) -> None:
        start = time.time()
        runtimes = [runner.execute() for runner in self.runners()]
        overall_runtime = time.time() - start

        Displayer("ALL", runtimes).display()
        self.save_as("all", runtimes)

        slow = list(filter(lambda runtime: runtime.runtime > self.slow, runtimes))
        Displayer("SLOW", slow).display()
        self.save_as("slow", slow)

        print(f"Overall runtime: {overall_runtime:.3f} seconds")

    def runners(self) -> list[LanguageRunner]:
        result: list[LanguageRunner] = []
        for day in self.days:
            for language in self.language_strategy.get(day):
                # 2023/25 is written in a randomized implementation
                # Average of multiple runs is more representative
                times = 10 if day == Day("2023", "25") else 1
                runner = LanguageRunner(
                    day=day,
                    name=language.name,
                    times=times,
                    command=language.run_command(day, self.run_args),
                )
                result.append(runner)
        return result

    def save_as(self, name: str, runtimes: list[RuntimeInfo]) -> None:
        if not self.save:
            return
        with open(f"{name}.json", "w") as f:
            value = [runtime.as_dict() for runtime in runtimes]
            f.write(json.dumps(value))
