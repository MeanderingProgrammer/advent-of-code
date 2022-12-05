# Advent of Code

Public Repo for Advent of Code Solutions

![Years Completed](advent-completed.png)

## Running

Use `runner/run.py` script to run various days rather than running directly.

Does lots of hacky stuff to set environment variables, compile common directories,
and set arguments to run commands.

Usage:

```
./runner/run.sh --years <years>? --days <days>?
```

* years: (optional) list of years to run, defaults to all years, example `2015 2019`
* days: (optional) list of days to run, defaults to all days, example `01 03 05`

## Generate Template

Generates initial files and empty data file for the specified language.

Will do any other required setup, such as updating `Cargo.toml` for `rust`.

Usage:

```
./template/generate.sh --year <year> --day <day> --lang <lang>
```

* year: Year to generate starting files for, example `2022`
* day: Day to generate starting files for, example `05`
* lang: Language to generate starting files for, must be supported, example `rust`

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
