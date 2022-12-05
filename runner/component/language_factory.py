from language.golang import Go
from language.java import Java
from language.python import Python
from language.rust import Rust


class LanguageFactory:

    def __init__(self):
        self.__extension_mapping = {
            '.go': Go(),
            '.java': Java(),
            '.py': Python(),
            '.rs': Rust(),
        }

    def get_language(self, solution_file):
        suffix = solution_file.suffix
        if suffix not in self.__extension_mapping:
            raise Exception(f'Unhandled suffix: {suffix}')
        return self.__extension_mapping[suffix]
