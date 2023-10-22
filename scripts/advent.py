#!/usr/bin/env python

import click
from typing import Optional, Tuple

from args.generate_template import GenerateTemplate
from args.run_template import RunTemplate
from command.generate import Generator
from command.run import Runner
from component.day_factory import DayFactory
from component.language_factory import LanguageFactory
from language.language import Language
from pojo.day import Day


class LanguageType(click.ParamType):
    name = "language"

    def convert(self, value, param, ctx) -> Language:
        factory = LanguageFactory()
        if value in factory.get_names():
            return factory.get_by_name(value)
        else:
            error = f"{value} is not a valid language: {factory.get_names()}"
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
        gen_day = GenerateTemplate().get(template)
    elif template is not None:
        raise Exception('If "year" or "day" is provided then "template" should not be')
    elif year is None or day is None:
        raise Exception('Both "year" and "day" are required if either is provided')
    else:
        gen_day = Day(year=str(year), day=str(day).zfill(2))

    generator = Generator(day=gen_day, language=language)
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
    year: Tuple[int],
    day: Tuple[int],
    language: Tuple[Language],
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
        raise Exception('If "year" or "day" is provided then "template" should not be')
    else:
        day_factory = DayFactory(
            years=[str(y) for y in year],
            days=[str(d).zfill(2) for d in day],
        )
        days = day_factory.get_days()

    if len(days) == 0:
        raise Exception("Could not find any days to run given input")

    languages = LanguageFactory().get_all() if len(language) == 0 else list(language)

    runner = Runner(
        days=days,
        languages=languages,
        slow=slow,
        run_args=["--test"] if test else [],
        save=template in ["days"] and len(language) == 0,
    )
    click.echo(f"{runner}") if info else runner.run()


if __name__ == "__main__":
    cli()
