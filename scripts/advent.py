#!/usr/bin/env python

from typing import Optional, override

import click
from args.generate_template import GenerateTemplate
from args.run_template import RunTemplate
from command.generate import Generator
from command.run import Runner
from component.day_factory import DayFactory
from component.language_factory import LanguageFactory
from component.language_strategy import LanguageStrategy
from language.language import Language


class LanguageType(click.ParamType):
    name = "language"
    factory = LanguageFactory()

    @override
    def get_metavar(self, param) -> str:
        return click.Choice(self.factory.get_names()).get_metavar(param)

    @override
    def convert(self, value: str, param, ctx) -> Language:
        if value in self.factory.get_names():
            return self.factory.get_by_name(value)
        else:
            error = f"{value} is not a valid language: {self.factory.get_names()}"
            self.fail(error, param, ctx)


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("-t", "--template", type=click.Choice(GenerateTemplate().get_names()))
@click.option("-y", "--year", type=int)
@click.option("-d", "--day", type=int)
@click.option("-l", "--language", type=LanguageType(), default="rust")
@click.option("-i", "--info", is_flag=True)
def generate(
    template: Optional[str],
    year: Optional[int],
    day: Optional[int],
    language: Language,
    info: bool,
) -> None:
    """
    Generates starting files for a specific day & language
    """

    if year is None and day is None:
        template = template or "next"
        days = [GenerateTemplate().get(template)]
    elif template is not None:
        raise Exception("If 'year' or 'day' is provided then 'template' should not be")
    elif year is None or day is None:
        raise Exception("Both 'year' and 'day' are required if either is provided")
    else:
        days = DayFactory(years=[year], days=[day]).get_days()

    assert len(days) == 1, "Can only generate one day at a time"
    generator = Generator(day=days[0], language=language)
    click.echo(f"{generator}") if info else generator.generate()


@cli.command()
@click.option("-t", "--template", type=click.Choice(RunTemplate().get_names()))
@click.option("-y", "--year", type=int, multiple=True)
@click.option("-d", "--day", type=int, multiple=True)
@click.option("-l", "--language", type=LanguageType(), multiple=True)
@click.option("-s", "--slow", type=int, default=5)
@click.option("-i", "--info", is_flag=True)
@click.option("--test", is_flag=True)
def run(
    template: Optional[str],
    year: tuple[int, ...],
    day: tuple[int, ...],
    language: tuple[Language, ...],
    slow: int,
    info: bool,
    test: bool,
) -> None:
    """
    Runs specific days / years for either specific or all languages
    """

    if len(year) == 0 and len(day) == 0:
        template = template or "latest"
        days = RunTemplate().get(template)
    elif template is not None:
        raise Exception("If 'year' or 'day' is provided then 'template' should not be")
    else:
        days = DayFactory(years=list(year), days=list(day)).get_days()

    if len(days) == 0:
        raise Exception("Could not find any days to run given input")

    language_strategy = LanguageStrategy(
        name="fastest" if template in ["latest", "days"] else "all",
        languages=LanguageFactory().get_all() if len(language) == 0 else list(language),
    )

    runner = Runner(
        days=days,
        language_strategy=language_strategy,
        slow=slow,
        run_args=["--test"] if test else [],
        save=template in ["days"] and len(language) == 0,
    )
    click.echo(f"{runner}") if info else runner.run()


if __name__ == "__main__":
    cli()
