#!/usr/bin/env python3

import click
from typing import List

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
def cli():
    pass


@cli.command()
@click.option("-t", "--template", type=click.Choice(GenerateTemplate().get_names()))
@click.option("-y", "--year", type=str)
@click.option("-d", "--day", type=str)
@click.option("-l", "--language", type=LanguageType(), default="rust")
@click.option("-i", "--info", is_flag=True)
def generate(
    template: str,
    year: str,
    day: str,
    language: Language,
    info: bool,
):
    """
    Generates starting files for a specific day & language
    """

    if year is None and day is None:
        template = template or "next"
        day = GenerateTemplate().get(template)
    elif template is not None:
        raise Exception('If "year" or "day" is provided then "template" should not be')
    elif year is None or day is None:
        raise Exception('Both "year" and "day" are required if either is provided')
    else:
        day = Day(year, day)

    generator = Generator(day, language)
    click.echo(f"{generator}") if info else generator.generate()


@cli.command()
@click.option("-t", "--template", type=click.Choice(RunTemplate().get_names()))
@click.option("-y", "--year", type=str, multiple=True)
@click.option("-d", "--day", type=str, multiple=True)
@click.option("-l", "--language", type=LanguageType())
@click.option("-i", "--info", is_flag=True)
@click.option("--test", is_flag=True)
def run(
    template: str,
    year: List[str],
    day: List[str],
    language: Language,
    info: bool,
    test: bool,
):
    """
    Runs specific days / years for either specific or all languages
    """

    if len(year) == 0 and len(day) == 0:
        template = template or "latest"
        days = RunTemplate().get(template)
    elif template is not None:
        raise Exception('If "year" or "day" is provided then "template" should not be')
    else:
        days = DayFactory(list(year), list(day)).get_days()

    if len(days) == 0:
        raise Exception("Could not find any days to run given input")

    languages = LanguageFactory().get_all() if language is None else [language]
    run_args = ["--test"] if test else []

    runner = Runner(days, languages, run_args)
    click.echo(f"{runner}") if info else runner.run()


if __name__ == "__main__":
    cli()
