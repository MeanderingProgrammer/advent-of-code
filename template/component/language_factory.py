from language.language import Language
from language.rust import Rust


class LanguageFactory:

    def __init__(self):
        self.__languages = [
            Rust(),
        ]
    
    def get_language(self, name) -> Language:
        supported = [language.name for language in self.__languages]
        if name not in supported:
            raise Exception(f'Language {name} is not one of {supported}')
        return [
            language 
            for language in self.__languages
            if language.name == name
        ][0]
