# Advent of Code

Public Repo for Advent of Code Solutions

![Years Completed](images/advent-completed.png)

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

Does some hacky stuff to set arguments and run commands, but for the most part runs
standard build commands for each language / framework.

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
  (--language <language>)* \
  --test? \
  --info?
```

| Variable Name | Alt  | Description                             | Default  | Example           |
| ------------- | ---- | --------------------------------------- | -------- | ----------------- |
| template      | `-t` | Name that targets specific years / days | `latest` | `-t languages`    |
| year          | `-y` | List of years to run                    | None     | `-y 2021 -y 2022` |
| day           | `-d` | List of days to run                     | None     | `-d 1 -d 3 -d 5`  |
| language      | `-l` | Limit runs to the specified languages   | None     | `-l golang`       |
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

Follow the instructions in the `README` of `aoc-cli` to get your session cookie setup.

This library relies on openssl which you will also need to install if you don't already have it.

Commands:

```
cargo install aoc-cli
touch .adventofcode.session
```

## Process Runtime Output

```
jq -r '.[]|[.year, .day, .language, .runtime]|@tsv' all.json
jq -r '.[]|select(.year == 2015 and .day == 24)' all.json
```

## Take Over 10 Seconds On Dell XPS 15

| Year | Day | Dell XPS 15 | M2 Mac  |
| ---- | --- | ----------- | ------- |
| 2017 | 17  | 0:16.39     | 0:04.73 |
| 2019 | 13  | 0:10.72     | 0:05.25 |
| 2019 | 19  | 0:11.89     | 0:05.21 |
| 2019 | 25  | 0:10.15     | 0:02.62 |
| 2020 | 22  | 0:10.24     | 0:03.80 |
