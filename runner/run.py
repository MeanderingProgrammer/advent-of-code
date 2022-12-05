import argparse
import os

from pathlib import Path
from typing import List

from component.display_runtimes import Displayer
from component.language_factory import LanguageFactory
from language.language import Language
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


def main(years: List[str], days: List[str]):
    factory = LanguageFactory()
    runtimes = get_runtimes(factory, years, days)
    print(runtimes)
    Displayer(runtimes).display()


def get_runtimes(
    factory: LanguageFactory, 
    years: List[str], 
    days: List[str],
) -> List[RuntimeInfo]:
    runtimes = []
    for year in years or get_dirs_wth_prefix('20'):
        print(f'Running year {year}')
        os.chdir(year)

        for day in days or get_dirs_wth_prefix(None):
            os.chdir(day)
            runtimes.extend(run_day(factory, Day(year, day)))

            # Change back out of day directory
            os.chdir('..')

        # Change back out of year directory
        os.chdir('..')
    return runtimes


def get_dirs_wth_prefix(valid_prefix):
    def prefix_predicate(dir_name):
        return valid_prefix is None or dir_name.startswith(valid_prefix)
    names = []
    for file_path in Path('.').iterdir():
        file_name = file_path.name
        if file_path.is_dir() and prefix_predicate(file_name):
            names.append(file_name)
    return names


def run_day(factory: LanguageFactory, day: Day) -> List[RuntimeInfo]:
    def is_solution_file(file_path):
        return file_path.is_file() and file_path.stem.lower() == 'solver'

    solution_files = [
        file_path 
        for file_path in Path('.').iterdir() 
        if is_solution_file(file_path)
    ]

    runtimes = []
    for solution_file in solution_files:
        language = factory.get_language(solution_file)
        runtime = run_language(language, day)
        runtimes.append(runtime)
    return runtimes


def run_language(language: Language, day: Day) -> RuntimeInfo:
    print(f'Running day {day.day} with {language.name}')
    language.setup()
    language.compile()
    runtime = language.run(day)
    print(f'Runtime: {runtime}')
    return RuntimeInfo(day, language.name, runtime)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--years', type=str, nargs='+')
    parser.add_argument('--days', type=str, nargs='+')

    args = parser.parse_args()
    main(args.years or [], args.days or [])
