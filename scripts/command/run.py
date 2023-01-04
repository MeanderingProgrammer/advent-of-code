import os
from pathlib import Path
from typing import List

from component.display_runtimes import Displayer
from component.language_factory import LanguageFactory
from language.language import Language
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


def do_run(days: List[Day], run_args: List[str]):
    factory = LanguageFactory()
    runtimes = get_runtimes(factory, days, run_args)
    Displayer(runtimes).display()


def get_runtimes(factory: LanguageFactory, days: List[Day], run_args: List[str]) -> List[RuntimeInfo]:
    runtimes = []
    for day in days:
        os.chdir(f'{day.year}/{day.day}')
        runtimes.extend(run_day(factory, day, run_args))
        # Change back out of day directory
        os.chdir('../..')
    return runtimes


def run_day(factory: LanguageFactory, day: Day, run_args: List[str]) -> List[RuntimeInfo]:
    def is_solution(file_path):
        return file_path.is_file() and file_path.stem.lower() == 'solver'
    solution_files = [file_path for file_path in Path('.').iterdir() if is_solution(file_path)]

    runtimes = []
    for solution_file in solution_files:
        language = factory.get_by_suffix(solution_file)
        runtime = run_language(language, day, run_args)
        runtimes.append(runtime)
    return runtimes


def run_language(language: Language, day: Day, run_args: List[str]) -> RuntimeInfo:
    print(f'Running year {day.year} day {day.day} with {language.name}')
    language.initial_setup()
    language.compile(day)
    runtime = language.run(day, run_args)
    print(f'Runtime: {runtime}')
    return RuntimeInfo(day, language.name, runtime)
