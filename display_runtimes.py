import pandas as pd
from termcolor import colored


def main():
    df = pd.read_csv('runtimes.csv')

    markdown = df.to_markdown(index=False)
    rows = markdown.split('\n')
    print('\n'.join(rows[:2]))
    for i, row in enumerate(rows[2:]):
        print(colored(row, get_color(df.iloc[i])))


def get_color(row):
    runtime = row['runtime']
    if runtime < 0.5:
        return 'green'
    elif runtime < 1.5:
        return None
    if runtime < 10:
        return 'yellow'
    else:
        return 'red'


if __name__ == '__main__':
    main()
