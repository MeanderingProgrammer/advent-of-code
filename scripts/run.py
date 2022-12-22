#!/usr/bin/env python3

import argparse
import os

from pathlib import Path
from typing import List

from component.day_factory import DayFactory
from component.display_runtimes import Displayer
from component.language_factory import LanguageFactory
from component.run_template import RunTemplate
from language.language import Language
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


def main(years: List[str], days: List[str], is_test: bool):
    run_days = DayFactory(years, days).get_days()
    if len(run_days) == 0:
        raise Exception('Could not find any days to run given input')
    factory = LanguageFactory()
    runtimes = get_runtimes(factory, run_days, is_test)
    Displayer(runtimes).display()


def get_runtimes(factory: LanguageFactory, days: List[Day], is_test: bool) -> List[RuntimeInfo]:
    runtimes = []
    for day in days:
        os.chdir(f'{day.year}/{day.day}')
        runtimes.extend(run_day(factory, day, is_test))
        # Change back out of day directory
        os.chdir('../..')
    return runtimes


def run_day(factory: LanguageFactory, day: Day, is_test: bool) -> List[RuntimeInfo]:
    def is_solution(file_path):
        return file_path.is_file() and file_path.stem.lower() == 'solver'
    solution_files = [file_path for file_path in Path('.').iterdir() if is_solution(file_path)]

    runtimes = []
    for solution_file in solution_files:
        language = factory.get_by_suffix(solution_file)
        runtime = run_language(language, day, is_test)
        runtimes.append(runtime)
    return runtimes


def run_language(language: Language, day: Day, is_test: bool) -> RuntimeInfo:
    print(f'Running year {day.year} day {day.day} with {language.name}')
    language.initial_setup()
    language.compile(day)
    runtime = language.run(day, is_test)
    print(f'Runtime: {runtime}')
    return RuntimeInfo(day, language.name, runtime)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--template', type=str)
    parser.add_argument('-y', '--years', type=str, nargs='+')
    parser.add_argument('-d', '--days', type=str, nargs='+')
    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    if args.years is None and args.days is None:
        template = args.template or 'latest'
        years, days = RunTemplate().get(template)
    elif args.template is not None:
        raise Exception('If --years or --days is provided then --template should not be')
    else:
        years, days = args.years or [], args.days or []

    main(years, days, args.test)
