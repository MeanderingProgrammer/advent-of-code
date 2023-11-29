from advent import run
from click.testing import CliRunner


def test_run_int_code() -> None:
    days: list[str] = []
    for day in [2] + list(range(5, 26, 2)):
        days.extend(["-d", str(day)])
    run_script(["-y", "19"] + days)


def test_run_go_batches() -> None:
    for year, day in [(15, 4), (16, 5), (16, 14)]:
        run_script(["-y", str(year), "-d", str(day), "-l", "golang"])


def run_script(args: list[str]) -> None:
    runner = CliRunner()
    result = runner.invoke(run, args)
    assert result.exit_code == 0
