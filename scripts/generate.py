#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

from component.language_factory import LanguageFactory
from pojo.day import Day


def main(day: Day, language_name: str):
    factory = LanguageFactory()
    language = factory.get_by_name(language_name)

    # Create date directory, okay if it already exists
    date_path = Path(day.year).joinpath(day.day)
    date_path.mkdir(parents=True, exist_ok=True)

    solution_path = date_path.joinpath(language.solution_file)
    if solution_path.exists():
        raise Exception(f'Solution already exists under: {solution_path}')
    
    template_file = f'scripts/templates/{language.solution_file}'
    print(f'Copying {template_file} to {solution_path}')
    os.system(f'cp {template_file} {solution_path}')
    
    data_path = date_path.joinpath('data.txt')
    if not data_path.exists():
        print(f'Creating data file under: {data_path}')
        data_path.touch()
    
    language.template_processing(day)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=str, required=True)
    parser.add_argument('--day', type=str, required=True)
    parser.add_argument('--lang', type=str, required=True)

    args = parser.parse_args()
    main(Day(args.year, args.day), args.lang)
