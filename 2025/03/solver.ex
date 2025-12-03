defmodule Solver do
  def main do
    Answer.timer(fn -> solution() end)
  end

  def solution do
    lines = Reader.lines()
    Answer.part1(17324, total(lines, 2))
    Answer.part2(171_846_613_143_331, total(lines, 12))
  end

  def total(lines, n) do
    lines
    |> Enum.map(fn line -> joltage(line, n, -1) end)
    |> Enum.map(fn value -> String.to_integer(value) end)
    |> Enum.sum()
  end

  def joltage(line, n, i) do
    if n <= 0 do
      ""
    else
      {ch, index} = next(line, n, i)
      ch <> joltage(line, n - 1, index)
    end
  end

  def next(line, n, i) do
    String.graphemes(line)
    |> Enum.with_index()
    |> Enum.take(String.length(line) - n + 1)
    |> Enum.drop(i + 1)
    |> Enum.max_by(fn {char, _} -> char end)
  end
end

Solver.main()
