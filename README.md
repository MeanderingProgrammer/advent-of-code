# Advent of Code

Public Repo for Advent of Code Solutions

![Years Completed](images/advent-completed.png)

# Setup

## Install Requirements

```
pip install -r scripts/requirements.txt
```

## Set Aliases

```
alias a_run="./scripts/advent.py run"
alias a_gen="./scripts/advent.py generate"
```

# Run

The `run` target is used to run various days rather than running directly.

Does some hacky stuff to set arguments and run commands, but for the most part runs
standard build commands for each language / framework.

None of the parameters are required, the default behavior in this case is to run the
latest day in the fastest language it is implemented in.

- Alias Command: `a_run`
- Direct Command: `./scripts/advent.py run`

## Usage

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

## Process Runtime Output

```
jq -r '.[]|[.year, .day, .language, .runtime]|@tsv' all.json
jq -r '.[]|[.year, .day, .language, .runtime]|@tsv' all.json | sort -nk4
jq -r '.[]|.runtime' all.json | awk '{ sum+=$1 } END { print "Seconds:", sum; print "Minutes:", sum / 60 }'
jq -r '.[]|[.year, .day, .runtime]|@tsv' all.json | sort -rnk3 | awk '{ if ($3 > 1) { print $0 } }'
jq -r '.[]|select(.year == 2015 and .day == 24)' all.json
```

# Generate

The `generate` target creates initial files and empty data file for the specified language.

Will do any other required setup, such as updating `Cargo.toml` for `rust`.

Will pull down your puzzle input if [instructions](#install-aoc-cli) are followed.

None of the parameters are required, the default behavior in this case is to generate the
next day using the rust template.

- Alias Command: `a_gen`
- Direct Command: `./scripts/advent.py generate`

## Usage

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

## Install aoc-cli

Template generation script can use `aoc-cli` to download input: [docs](https://github.com/scarvalhojr/aoc-cli).

Follow the instructions in the `README` of `aoc-cli` to get your session cookie setup.

This library relies on openssl which you will also need to install if you don't already have it.

```
cargo install aoc-cli
touch .adventofcode.session
```

# Take over 1 second on M2 Mac

| Year | Day | Runtime | Status | Notes                                                   |
| ---- | --- | ------- | ------ | ------------------------------------------------------- |
| 2018 | 15  | 5.042   | LEAVE  | Complex game state with path finding between characters |
| 2018 | 19  | 4.878   | LEAVE  | Kinda like int-code but running it seems not feesible   |
| 2022 | 16  | 4.603   | LEAVE  | Path finding with multiple agents is fairly optimized   |
| 2016 | 5   | 4.576   | MAYBE  | Final md5 hash that hasn't been optimized with batches  |
| 2021 | 23  | 3.247   | UNSURE | Looks like a complex path finding problem               |
| 2019 | 18  | 2.235   | LEAVE  | Mostly the Java runtime for such a small execution      |
| 2016 | 25  | 2.018   | TODO   | Kinda like int-code, can probably make it faster        |
| 2016 | 11  | 2.009   | LEAVE  | That chips and generator problem, not fun               |
| 2019 | 17  | 1.993   | TODO   | Normal int-code that hasn't been moved to Rust          |
| 2020 | 11  | 1.989   | TODO   | N/A                                                     |
| 2019 | 9   | 1.850   | TODO   | Normal int-code that hasn't been moved to Rust          |
| 2016 | 14  | 1.664   | LEAVE  | Already batched implementation of md5                   |
| 2019 | 23  | 1.621   | TODO   | Normal int-code that hasn't been moved to Rust          |
| 2019 | 24  | 1.607   | TODO   | Game of life problem, optimized by using tuples         |
| 2020 | 15  | 1.552   | MAYBE  | Even in Rust iterating to 30,000,000 takes a bit        |
| 2015 | 18  | 1.495   | TODO   | Optimized with tuples, probably need to move to Rust    |
| 2021 | 12  | 1.490   | TODO   | Path finding problem, might be some room to improve     |
| 2022 | 15  | 1.483   | LEAVE  | Dealing with large space, already in Rust               |
| 2019 | 25  | 1.419   | LEAVE  | Mostly spends time permuting through the items          |
| 2018 | 22  | 1.396   | TODO   | N/A                                                     |
| 2018 | 3   | 1.392   | TODO   | N/A                                                     |
| 2015 | 10  | 1.356   | TODO   | Growing list, Rust can probably fix it                  |
| 2018 | 18  | 1.350   | TODO   | Game of life problem, optimized by using tuples         |
| 2018 | 14  | 1.304   | MAYBE  | Would need to be a lot more clever to get better        |
| 2017 | 22  | 1.288   | MAYBE  | Game of life problem already in Rust                    |
| 2017 | 21  | 1.273   | TODO   | N/A                                                     |
| 2018 | 24  | 1.229   | TODO   | Complex game, fairly optimized in Python                |
| 2016 | 24  | 1.199   | TODO   | N/A                                                     |
| 2019 | 20  | 1.132   | LEAVE  | Mostly the Java runtime for such a small execution      |
| 2017 | 3   | 1.109   | TODO   | Can probably improve by using a dict / tuple            |
| 2015 | 13  | 1.048   | TODO   | Mostly likely slowed by the permutation computation     |
| 2018 | 6   | 1.002   | TODO   | Most of the computation is in the distance logic        |
