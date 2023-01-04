#!/usr/bin/env python3

import click

from command.generate import generate
from command.run import run

from args.generate_template import GenerateTemplate
from pojo.day import Day

@click.group()
def cli():
    pass

@cli.command()
@click.option('-t', '--template', type=str)
@click.option('-y', '--year', type=int)
@click.option('-d', '--day', type=str)
@click.option('-l', '--lang', type=str, default='rust')
@click.option('-i', '--info', is_flag=True)
def generate(template: str, year: int, day: int, lang: str, info: bool):
    click.echo(f'This is generate() with')
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
        #generate(day, lang)
        print('hi', day, lang)

@cli.command()
@click.option('-t', '--template', type=str)
@click.option('-y', '--years', type=int)
@click.option('-d', '--days', type=str)
@click.option('-i', '--info', is_flag=True)
@click.option('--test', is_flag=True)
def run(template, years):
    click.echo('This is run()')
    # run()

if __name__ == '__main__':
    cli()
