#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

from component.language_factory import LanguageFactory
from language.language import Language
from pojo.day import Day

ADVENT_COOKIE_FILE = '.adventofcode.session'


def main(day: Day, language_name: str):
    language = LanguageFactory().get_by_name(language_name)
    date_path = get_date_path(day)

    solution_path = get_solution_path(language, date_path)
    # At this point we can assume this is the first time we are processing
    # this day for this language, since the solution path does not exist
    language.template_processing(day)

    copy_template_to(language, solution_path)
    create_sample_if_necessary(date_path)
    create_data_if_necessary(day, date_path)


def get_date_path(day: Day) -> Path:
    # Create date directory, okay if it already exists
    date_path = Path(day.year).joinpath(day.day)
    date_path.mkdir(parents=True, exist_ok=True)
    return date_path


def get_solution_path(language: Language, date_path: Path) -> Path:
    solution_path = date_path.joinpath(language.solution_file)
    if solution_path.exists():
        raise Exception(f'Solution already exists under: {solution_path}')
    return solution_path


def copy_template_to(language: Language, solution_path: Path):
    template_file = f'scripts/templates/{language.solution_file}'
    print(f'Copying {template_file} to {solution_path}')
    os.system(f'cp {template_file} {solution_path}')


def create_sample_if_necessary(date_path: Path):
    sample_path = date_path.joinpath('sample.txt')
    if not sample_path.exists():
        print(f'Creating empty {sample_path}')
        sample_path.touch()


def create_data_if_necessary(day: Day, date_path: Path):
    data_path = date_path.joinpath('data.txt')
    if not data_path.exists():
        print(f'Creating data file under: {data_path}')
        if Path(ADVENT_COOKIE_FILE).exists():
            print('Downloading input using aoc-cli')
            download_input(day, data_path)
        else:
            print(f'Creating empty {data_path} since aoc-cli is not setup')
            data_path.touch()
    else:
        print(f'{data_path} already exists, leaving as is')


def download_input(day: Day, data_path):
    os.system(f'''aoc download  \\
        --year {day.year} --day {day.day} \\
        --input-file {data_path} \\
        --input-only \\
        --session-file ./.adventofcode.session''')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year', type=str, required=True)
    parser.add_argument('-d', '--day', type=str, required=True)
    parser.add_argument('-l', '--lang', type=str, required=True)

    args = parser.parse_args()
    main(Day(args.year, args.day), args.lang)
