import re
import time
from dataclasses import dataclass
from typing import Any

from component.command import Executor
from component.display_runtimes import Displayer
from component.history import History
from component.language_strategy import LanguageStrategy
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class LanguageRunner:
    day: Day
    name: str
    times: int
    command: list[str]
    executor: Executor

    def as_dict(self) -> dict[str, Any]:
        return dict(
            year=self.day.year,
            day=self.day.day,
            name=self.name,
            times=self.times,
            command=" ".join(self.command),
        )

    def execute(self) -> RuntimeInfo:
        print(f"Running {self.day.dir()} with {self.name} ({self.times})")

        runtimes: list[float] = []
        executions: list[float] = []
        for _ in range(self.times):
            runtime, execution = self.run_command(self.command)
            runtimes.append(runtime)
            executions.append(execution)

        return RuntimeInfo(
            day=self.day,
            language=self.name,
            runtime=sum(runtimes) / self.times,
            execution=sum(executions) / self.times,
        )

    def run_command(self, command: list[str]) -> tuple[float, float]:
        start = time.time_ns()
        result = self.executor.run(command)
        execution_ns = float(time.time_ns() - start)

        assert "Part 1:" in result, "Must have answer to part 1"
        if int(self.day.day) < 25:
            assert "Part 2:" in result, "Must have answer to part 2"

        matches: list[str] = re.findall(r".*Runtime \(ns\): (\d*)", result)
        assert len(matches) == 1, "Could not find runtime in output"
        runtime_ns = float(matches[0])

        return (runtime_ns / 1_000_000, execution_ns / 1_000_000)


@dataclass(frozen=True)
class Runner:
    days: list[Day]
    language_strategy: LanguageStrategy
    slow: int
    args: list[str]
    save: bool

    def info(self) -> dict[str, Any]:
        return dict(
            executions=[runner.as_dict() for runner in self.runners()],
            slow=self.slow,
            save=self.save,
        )

    def run(self) -> None:
        start = time.time()
        runtimes = [runner.execute() for runner in self.runners()]
        overall_runtime = time.time() - start

        slow = list(filter(lambda runtime: runtime.runtime > self.slow, runtimes))
        previous = History("all").load(False)
        Displayer("all", runtimes, previous).display()
        Displayer("slow", slow, previous).display()

        if self.save:
            History("all").save(runtimes)
            History("slow").save(slow)

        print(f"Overall runtime: {overall_runtime:.3f} seconds")

    def runners(self) -> list[LanguageRunner]:
        executor = Executor()
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
                    command=language.run(day, self.args),
                    executor=executor,
                )
                result.append(runner)
        return result
