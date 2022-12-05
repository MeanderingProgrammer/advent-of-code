from pathlib import Path
from typing import List, Tuple


class RunTemplate:

    def __init__(self):
        self.__template_mapping = {
            'all_languages': self.__get_all_languages,
            'latest': self.__get_latest,
        }

    def get(self, name) -> Tuple[List[str], List[str]]:
        valid_values = list(self.__template_mapping.keys())
        if name not in valid_values:
            raise Exception(f'Unknown template {name}, should be one of {valid_values}')
        return self.__template_mapping[name]()
    
    def __get_latest(self) -> Tuple[List[str], List[str]]:
        year = self.__get_sorted_dirs('.', '20')
        day = self.__get_sorted_dirs(year, None)
        return (
            [year],
            [day],
        )
    
    @staticmethod
    def __get_sorted_dirs(start, prefix):
        def prefix_predicate(dir_name):
            return prefix is None or dir_name.startswith(prefix)

        paths = [
            file_path.name
            for file_path in Path(start).iterdir()
            if file_path.is_dir() and prefix_predicate(file_path.name)
        ]
        paths.sort(reverse=True)
        return paths[0]
    
    @staticmethod
    def __get_all_languages() -> Tuple[List[str], List[str]]:
        # Python = 2019 - 01
        # Java = 2019 - 20
        # Rust & Go = 2021 - 01
        return (
            ['2019', '2021'],
            ['01', '20'],
        )
