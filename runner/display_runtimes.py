import os
import pandas as pd
from termcolor import colored


def display(runtimes):
    df = pd.DataFrame(runtimes)
    _print_df('ALL', df)
    _print_df('SLOW', df[df['runtime'] > 10])


def _print_df(label, df):
    if df.shape[0] == 0:
        print('{}: NONE'.format(label))
        return

    print(label)
    markdown = df.to_markdown(index=False)
    rows = markdown.split('\n')
    print('\n'.join(rows[:2]))
    for i, row in enumerate(rows[2:]):
        print(colored(row, _get_color(df.iloc[i])))


def _get_color(row):
    color_predicates = {
        'green': lambda x: 0 <= x < 0.5,
        'yellow': lambda x: 0.5 <= x < 10,
        'red': lambda x: 10 <= x,
    }
    for color, predicate in color_predicates.items():
        if predicate(row['runtime']):
            return color
