from language.golang import Go
from language.java import Java
from language.language import Language
from language.python import Python
from language.rust import Rust


class LanguageFactory:

    def __init__(self) -> str:
        self.__languages = [
            Go(),
            Java(),
            Python(),
            Rust(),
        ]

    def get_by_suffix(self, solution_file) -> Language:
        return self._get_by(solution_file.suffix, lambda x: x.suffix)
    
    def get_by_name(self, name) -> Language:
        return self._get_by(name, lambda x: x.name)
    
    def _get_by(self, value, extractor) -> Language:
        mapping = { extractor(language): language for language in self.__languages }
        if value not in mapping:
            raise Exception(f'{value} is not one of {list(mapping.keys())}')
        return mapping[value]
