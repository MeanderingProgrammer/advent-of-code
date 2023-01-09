#!/usr/bin/env python3

import click
from typing import List

from args.generate_template import GenerateTemplate
from args.run_template import RunTemplate
from command.generate import Generator
from command.run import Runner
from component.day_factory import DayFactory
from pojo.day import Day


@click.group()
def cli():
    pass


@cli.command()
@click.option('-t', '--template', type=str)
@click.option('-y', '--year', type=str)
@click.option('-d', '--day', type=str)
@click.option('-l', '--lang', type=str, default='rust')
@click.option('-i', '--info', is_flag=True)
def generate(template: str, year: str, day: str, lang: str, info: bool):
    if year is None and day is None:
        template = template or 'next'
        day = GenerateTemplate().get(template)
    elif template is not None:
        raise Exception('If "year" or "day" is provided then "template" should not be')
    elif year is None or day is None:
        raise Exception('Both "year" and "day" are required if either is provided')
    else:
        day = Day(year, day)

    if info:
        click.echo(f'Would generate files for {day} in {lang}')
    else:
        Generator(day, lang).generate()


@cli.command()
@click.option('-t', '--template', type=str)
@click.option('-y', '--year', type=str, multiple=True)
@click.option('-d', '--day', type=str, multiple=True)
@click.option('-i', '--info', is_flag=True)
@click.option('--test', is_flag=True)
def run(template: str, year: List[str], day: List[str], info: bool, test: bool):
    if len(year) == 0 and len(day) == 0:
        template = template or 'latest'
        days = RunTemplate().get(template)
    elif template is not None:
        raise Exception('If "year" or "day" is provided then "template" should not be')
    else:
        days = DayFactory(list(year), list(day)).get_days()

    if len(days) == 0:
        raise Exception('Could not find any days to run given input')

    run_args = []
    if test:
        run_args.append('--test')

    if info:
        click.echo(f'Would run {days} with {run_args}')
    else:
        Runner(days, run_args).run()


if __name__ == '__main__':
    cli()
