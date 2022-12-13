# Advent of Code

Public Repo for Advent of Code Solutions

![Years Completed](advent-completed.png)

## Running

Use `scripts/run.py` script to run various days rather than running directly.

Does lots of hacky stuff to set environment variables, compile common directories,
and set arguments to run commands.

Usage:

```
./scripts/run.py --template <template>? --years <years>? --days <days>?
```

| Variable Name | Alt  | Description                             | Required  | Default  | Example         |
| ------------- | ---- | --------------------------------------- | --------- | -------- | --------------- |
| template      | `-t` | Name that targets specific years / days | False     | `latest` | `all_languages` |
| years         | `-y` | List of years to run                    | False     | None     | `2022`          |
| days          | `-d` | List of days to run                     | False     | None     | `01 03 05`      |

* If `template` is provided then `years` & `days` must not be provided
* If  `years` or `days` are provided then `template` must not be provided

## Generate Template

Generates initial files and empty data file for the specified language.

Will do any other required setup, such as updating `Cargo.toml` for `rust`.

Usage:

```
./scripts/generate.py --template <template>? --year <year>? --day <day>? --lang <lang>?
```

| Variable Name | Alt  | Description                              | Required  | Default | Example  |
| ------------- | ---- | ---------------------------------------- | --------- | ------- | -------- |
| template      | `-t` | Name that targets specific year / day    | False     | `next`  | `next`   |
| year          | `-y` | Year to generate starting files for      | False     | None    | `2022`   |
| day           | `-d` | Day to generate starting files for       | False     | None    | `05`     |
| lang          | `-l` | Language to generate starting files for  | False     | `rust`  | `python` |

* If `template` is provided then `year` & `day` must not be provided
* If  `year` or `day` are provided then `template` must not be provided

### Install aoc-cli

Template generation script can use `aoc-cli` to download input: [docs](https://github.com/scarvalhojr/aoc-cli).

* The presense of the `.adventofcode.session` in the repo top level directory enables this logic
* To set this up create the file and follow the instructions in the `README` of `aoc-cli` to get your session cookie

This library relies on openssl which you will also need to install if you don't already have it.

Commands:

```
sudo apt-get install pkg-config libssl-dev
cargo install aoc-cli
touch .adventofcode.session
```

## Take Over 10 Seconds (On My Decent Laptop)

| Year | Day  | Time    |
| ---- | ---- | ------- |
| 2015 | 10   | 0:15.86 |
| 2015 | 18   | 0:26.12 |
| 2015 | 20   | 0:14.64 |
| 2015 | 22   | 0:22.70 |
| 2015 | 24   | 0:12.34 |
| 2016 | 5    | 0:37.48 |
| 2016 | 11   | 1:51.17 |
| 2016 | 12   | 0:35.69 |
| 2016 | 14   | 0:35.59 |
| 2016 | 18   | 0:26.21 |
| 2017 | 14   | 0:14.21 |
| 2017 | 15   | 1:21.71 |
| 2017 | 17   | 0:38.75 |
| 2017 | 22   | 1:02.91 |
| 2017 | 25   | 1:09.87 |
| 2018 | 5    | 0:10.89 |
| 2018 | 6    | 0:20.15 |
| 2018 | 10   | 0:10.61 |
| 2018 | 11   | 1:28.29 |
| 2018 | 14   | 0:35.87 |
| 2018 | 15   | 3:59.39 |
| 2018 | 18   | 1:09.36 |
| 2018 | 19   | 0:16.66 |
| 2018 | 24   | 0:10.01 |
| 2019 | 12   | 0:18.32 |
| 2019 | 13   | 0:24.05 |
| 2019 | 16   | 0:12.88 |
| 2019 | 19   | 0:17.07 |
| 2019 | 21   | 0:10.37 |
| 2019 | 24   | 0:20:31 |
| 2019 | 25   | 1:52.72 |
| 2020 | 11   | 0:14.67 |
| 2020 | 15   | 0:58.97 |
| 2020 | 23   | 0:21.99 |
| 2020 | 24   | 0:13.45 |
