import os
import pandas as pd
from termcolor import colored


def main():
    df = pd.read_csv('{}/runtimes.csv'.format(os.path.dirname(__file__)))
    print_df('ALL', df)
    print_df('SLOW', df[df['runtime'] > 10])


def print_df(label, df):
    if df.shape[0] == 0:
        print('{}: NONE'.format(label))
        return

    print(label)
    markdown = df.to_markdown(index=False)
    rows = markdown.split('\n')
    print('\n'.join(rows[:2]))
    for i, row in enumerate(rows[2:]):
        print(colored(row, get_color(df.iloc[i])))


def get_color(row):
    runtime = row['runtime']
    color_predicates = {
        'green': lambda x: 0 <= x < 0.5,
        'yellow': lambda x: 0.5 <= x < 10,
        'red': lambda x: 10 <= x,
    }
    for color, predicate in color_predicates.items():
        if predicate(row['runtime']):
            return color


if __name__ == '__main__':
    main()
