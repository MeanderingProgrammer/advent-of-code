from pathlib import Path

from aoc.parser import Parser


def test_string(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["abcd", "efg"])
    assert "abcd\nefg" == parser(path).string()


def test_integer(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["123", ""])
    assert 123 == parser(path).integer()


def test_int_string(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["1312113"])
    assert [1, 3, 1, 2, 1, 1, 3] == parser(path).int_string()


def test_entries(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["abcd efg"])
    assert ["abcd", "efg"] == parser(path).entries()


def test_int_entries(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["123 -12 1"])
    assert [123, -12, 1] == parser(path).int_entries()


def test_csv(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["abcd,efg"])
    assert ["abcd", "efg"] == parser(path).csv()


def test_int_csv(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["123,-12,1"])
    assert [123, -12, 1] == parser(path).int_csv()


def test_lines(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["abcd", "efg"])
    assert ["abcd", "efg"] == parser(path).lines()


def test_int_lines(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["123", "-12", "1"])
    assert [123, -12, 1] == parser(path).int_lines()


def test_nested_lines(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["abcd", "efg"])
    assert [["a", "b", "c", "d"], ["e", "f", "g"]] == parser(path).nested_lines()


def test_line_groups(tmp_path: Path) -> None:
    path = new_file(tmp_path, ["abcd", "efg", "", "hij"])
    assert [["abcd", "efg"], ["hij"]] == parser(path).line_groups()


def new_file(path: Path, lines: list[str]) -> Path:
    data = path / "data.txt"
    with data.open("w") as f:
        f.write("\n".join(lines))
    return data


def parser(path: Path) -> Parser:
    return Parser(file_name=str(path), data_file=False)
