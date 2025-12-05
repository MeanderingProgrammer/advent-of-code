defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    lines = Reader.lines()
    Answer.part1(17324, total(lines, 2))
    Answer.part2(171_846_613_143_331, total(lines, 12))
  end

  @spec total([String.t()], pos_integer()) :: integer()
  def total(lines, n) do
    lines
    |> Enum.map(&joltage(&1, n, -1))
    |> Enum.map(&String.to_integer/1)
    |> Enum.sum()
  end

  @spec joltage(String.t(), integer(), integer()) :: String.t()
  def joltage(line, n, i) do
    case n do
      0 ->
        ""

      _ ->
        {ch, index} = next(line, n, i)
        ch <> joltage(line, n - 1, index)
    end
  end

  @spec next(String.t(), integer(), integer()) :: {String.t(), integer()}
  def next(line, n, i) do
    String.graphemes(line)
    |> Enum.with_index()
    |> Enum.slice((i + 1)..(String.length(line) - n))
    |> Enum.max_by(&elem(&1, 0))
  end
end

Solver.main()
