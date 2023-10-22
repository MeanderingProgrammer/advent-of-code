# Advent of Code

Public Repo for Advent of Code Solutions

![Years Completed](advent-completed.png)

## Install Requirements

```
pip install -r scripts/requirements.txt
```

## Set Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```
# Advent Aliases
alias a_run="./scripts/advent.py run"
alias a_gen="./scripts/advent.py generate"
```

## Running a Day

Used to run various days rather than running directly.

Does lots of hacky stuff to set environment variables, compile common directories,
and set arguments to run commands.

None of the parameters are required, the default behavior in this case is to run the
latest day in all languages it is implemented in.

- Alias Command: `a_run`
- Direct Command: `./scripts/advent.py run`

### Usage

```
a_run \
  --template <template>? \
  (--year <year>)* \
  (--day <day>)* \
  --language <language>? \
  --test? \
  --info?
```

| Variable Name | Alt  | Description                             | Default  | Example           |
| ------------- | ---- | --------------------------------------- | -------- | ----------------- |
| template      | `-t` | Name that targets specific years / days | `latest` | `-t all_langs`    |
| year          | `-y` | List of years to run                    | None     | `-y 2021 -y 2022` |
| day           | `-d` | List of days to run                     | None     | `-d 1 -d 3 -d 5`  |
| language      | `-l` | Limit runs to the specified language    | None     | `-l golang`       |
| test          | N/A  | Passes test flag to each day            | `False`  | `--test`          |
| info          | `-i` | Outputs which days would run            | `False`  | `-i`              |

- If `template` is provided then `year` & `day` must not be provided
- If `year` or `day` are provided then `template` must not be provided

## Generate Template

Generates initial files and empty data file for the specified language.

Will do any other required setup, such as updating `Cargo.toml` for `rust`.

Will pull down your puzzle input if [instructions](##install-aoc-cli) are followed.

None of the parameters are required, the default behavior in this case is to generate the
next day using the rust template.

- Alias Command: `a_gen`
- Direct Command: `./scripts/advent.py generate`

### Usage

```
a_gen \
  --template <template>? \
  --year <year>? \
  --day <day>? \
  --language <language>? \
  --info?
```

| Variable Name | Alt  | Description                             | Default | Example     |
| ------------- | ---- | --------------------------------------- | ------- | ----------- |
| template      | `-t` | Name that targets specific year / day   | `next`  | `-t next`   |
| year          | `-y` | Year to generate starting files for     | None    | `-y 2022`   |
| day           | `-d` | Day to generate starting files for      | None    | `-d 5`      |
| language      | `-l` | Language to generate starting files for | `rust`  | `-l python` |
| info          | `-i` | Outputs which day would get generated   | `False` | `-i`        |

- If `template` is provided then `year` & `day` must not be provided
- If `year` or `day` are provided then `template` must not be provided

### Install aoc-cli

Template generation script can use `aoc-cli` to download input: [docs](https://github.com/scarvalhojr/aoc-cli).

- The presense of the `.adventofcode.session` in the repo top level directory enables this logic
- To set this up create the file and follow the instructions in the `README` of `aoc-cli` to get your session cookie

This library relies on openssl which you will also need to install if you don't already have it.

Commands:

```
sudo apt-get install pkg-config libssl-dev
cargo install aoc-cli
touch .adventofcode.session
```

## Take Over 10 Seconds On Dell XPS 15

| Year | Day | Dell XPS 15 | M2 Mac  |
| ---- | --- | ----------- | ------- |
| 2015 | 10  | 0:11.21     | 0:05.22 |
| 2015 | 20  | 0:12.22     | 0:06.73 |
| 2015 | 22  | 0:14.09     | 0:07.63 |
| 2015 | 24  | 0:10.47     | 0:05.08 |
| 2017 | 14  | 0:11.54     | 0:04.97 |
| 2017 | 17  | 0:16.39     | 0:04.73 |
| 2018 | 6   | 0:11.18     | 0:05:02 |
| 2018 | 15  | 0:17.16     | 0:06.66 |
| 2018 | 18  | 0:16.59     | 0:07.83 |
| 2019 | 13  | 0:15.24     | 0:07.19 |
| 2019 | 19  | 0:10.26     | 0:05.00 |
| 2019 | 24  | 0:11.78     | 0:05.73 |
