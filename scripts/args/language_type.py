from typing import override

import click
from component.language_factory import LanguageFactory
from language.language import Language


class LanguageType(click.ParamType):
    name = "language"
    factory = LanguageFactory()

    @override
    def get_metavar(self, param) -> str:
        return click.Choice(self.factory.names()).get_metavar(param)

    @override
    def convert(self, value: str, param, ctx) -> Language:
        if value in self.factory.names():
            return self.factory.from_name(value)
        else:
            error = f"{value} is not a valid language: {self.factory.names()}"
            self.fail(error, param, ctx)
