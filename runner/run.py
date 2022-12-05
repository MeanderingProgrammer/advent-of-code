import argparse
import os
import time
import pandas as pd
from pathlib import Path
from display_runtimes import display
from language_factory import LanguageFactory
from pojo.day import Day


def main(years, days):
    runtimes = []
    factory = LanguageFactory()

    for year in years or get_all('20'):
        print(f'Running year {year}')
        os.chdir(year)

        for day in days or get_all(None):
            os.chdir(day)
            run_day(runtimes, factory, Day(year, day))

            # Change back out of day directory
            os.chdir('..')

        # Change back out of year directory
        os.chdir('..')
    
    display(pd.DataFrame(runtimes))


def get_all(valid_prefix):
    names = []
    for file_path in Path('.').iterdir():
        if file_path.is_dir() and (valid_prefix is None or file_path.name.startswith(valid_prefix)):
            names.append(file_path.name)
    return names


def run_day(runtimes, factory, day):
    solution_files = [file_path for file_path in Path('.').iterdir() if is_solution(file_path)]
    for solution_file in solution_files:
        language = factory.get_language(solution_file)
        print(f'Running day {day.day} with {language.name}')
        runtime = run(language, day)
        print(f'Runtime: {runtime}')
        runtimes.append({
            'year': day.year,
            'day': day.day,
            'language': language.name,
            'runtime': runtime,
        })


def is_solution(file_path):
    return file_path.is_file() and file_path.stem.lower() == 'solver'


def run(langugage, day):
    langugage.setup()
    langugage.compile()

    start = time.time()
    langugage.run(day)
    return time.time() - start


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--years', type=str, nargs='+')
    parser.add_argument('--days', type=str, nargs='+')

    args = parser.parse_args()
    main(args.years, args.days)
