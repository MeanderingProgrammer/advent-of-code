import os
from pathlib import Path

from component.language_factory import LanguageFactory
from language.language import Language
from pojo.day import Day

ADVENT_COOKIE_FILE = '.adventofcode.session'


class Generator:

    def __init__(self, day: Day, language_name: str):
        self.__day: Day = day
        self.__language: Language = LanguageFactory().get_by_name(language_name)

    def generate(self):
        date_path = self.__get_date_path()

        solution_path = self.__get_solution_path(date_path)
        # At this point we can assume this is the first time we are processing
        # this day for this language, since the solution path does not exist
        self.__language.template_processing(self.__day)

        self.__copy_template_to(solution_path)
        self.__create_sample_if_necessary(date_path)
        self.__create_data_if_necessary(date_path)

    def __get_date_path(self) -> Path:
        # Create date directory, okay if it already exists
        date_path = Path(self.__day.year).joinpath(self.__day.day)
        date_path.mkdir(parents=True, exist_ok=True)
        return date_path

    def __get_solution_path(self, date_path: Path) -> Path:
        solution_path = date_path.joinpath(self.__language.solution_file)
        if solution_path.exists():
            raise Exception(f'Solution already exists under: {solution_path}')
        return solution_path

    def __copy_template_to(self, solution_path: Path):
        template_file = f'scripts/templates/{self.__language.solution_file}'
        print(f'Copying {template_file} to {solution_path}')
        os.system(f'cp {template_file} {solution_path}')

    def __create_sample_if_necessary(self, date_path: Path):
        sample_path = date_path.joinpath('sample.txt')
        if not sample_path.exists():
            print(f'Creating empty {sample_path}')
            sample_path.touch()

    def __create_data_if_necessary(self, date_path: Path):
        data_path = date_path.joinpath('data.txt')
        if not data_path.exists():
            print(f'Creating data file under: {data_path}')
            if Path(ADVENT_COOKIE_FILE).exists():
                print('Downloading input using aoc-cli')
                self.__download_input(data_path)
            else:
                print(f'Creating empty {data_path} since aoc-cli is not setup')
                data_path.touch()
        else:
            print(f'{data_path} already exists, leaving as is')

    def __download_input(self, data_path: Path):
        os.system(f'''aoc download  \\
            --year {self.__day.year} --day {self.__day.day} \\
            --input-file {data_path} \\
            --input-only \\
            --session-file ./.adventofcode.session''')
