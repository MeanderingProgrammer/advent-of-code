#!/usr/bin/env python

from typing import Optional

import click
from args.generate_template import GenerateName, GenerateTemplate
from args.language_type import LanguageType
from args.run_template import RunName, RunTemplate
from args.str_enum_type import StrEnumType
from command.generate import Generator
from command.graph import Grapher
from command.run import Runner
from component.day_factory import DayFactory
from component.language_factory import LanguageFactory
from component.language_strategy import LanguageStrategy, StrategyName
from language.language import Language


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("-t", "--template", type=StrEnumType(RunName))
@click.option("-y", "--year", type=int, multiple=True)
@click.option("-d", "--day", type=int, multiple=True)
@click.option("-l", "--language", type=LanguageType(), multiple=True)
@click.option("-s", "--slow", type=int, default=1)
@click.option("-i", "--info", is_flag=True)
@click.option("--test", is_flag=True)
def run(
    template: Optional[RunName],
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
        template = template or RunName.LATEST
        days = RunTemplate().get(template)
    elif template is not None:
        raise Exception("If 'year' or 'day' is provided then 'template' should not be")
    else:
        days = DayFactory(years=list(year), days=list(day)).get_days()

    if len(days) == 0:
        raise Exception("Could not find any days to run given input")

    fast = [RunName.LATEST, RunName.DAYS, RunName.BATCHES]
    language_strategy = LanguageStrategy(
        name=StrategyName.FASTEST if template in fast else StrategyName.ALL,
        languages=LanguageFactory().get_all() if len(language) == 0 else list(language),
    )

    runner = Runner(
        days=days,
        language_strategy=language_strategy,
        slow=slow,
        run_args=["--test"] if test else [],
        save=template in [RunName.DAYS] and len(language) == 0,
    )
    click.echo(f"{runner}") if info else runner.run()


@cli.command()
@click.option("-t", "--template", type=StrEnumType(GenerateName))
@click.option("-y", "--year", type=int)
@click.option("-d", "--day", type=int)
@click.option("-l", "--language", type=LanguageType(), default="rust")
@click.option("-i", "--info", is_flag=True)
def generate(
    template: Optional[GenerateName],
    year: Optional[int],
    day: Optional[int],
    language: Language,
    info: bool,
) -> None:
    """
    Generates starting files for a specific day & language
    """
    if year is None and day is None:
        template = template or GenerateName.NEXT
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
@click.option("-a", "--archive", is_flag=True)
@click.option("-i", "--info", is_flag=True)
def graph(archive: bool, info: bool) -> None:
    """
    Creates some fun graphs based on runtimes
    """
    grapher = Grapher(archive=archive)
    click.echo(f"{grapher}") if info else grapher.graph()


if __name__ == "__main__":
    cli()
