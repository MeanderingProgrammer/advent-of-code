from typing import override

import click

from component.language_factory import LanguageFactory
from language.language import Language


class LanguageType(click.ParamType):
    name: str = "language"
    factory: LanguageFactory = LanguageFactory()

    @override
    def get_metavar(self, param: click.Parameter, ctx: click.Context) -> str | None:
        return click.Choice(self.factory.names()).get_metavar(param, ctx)

    @override
    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> Language:
        result = self.factory.get(value)
        if result is None:
            message = f"{value} is not a valid language: {self.factory.names()}"
            self.fail(message, param, ctx)
        return result
