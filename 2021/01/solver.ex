defmodule Solver do
  def main do
    Answer.timer(fn -> solution() end)
  end

  def solution do
    lines = Reader.lines()
    values = lines |> Enum.map(fn s -> String.to_integer(s) end)
    Answer.part1(1292, window_increases(values, 1))
    Answer.part2(1262, window_increases(values, 3))
  end

  def window_increases(values, window_size) do
    Enum.chunk_every(values, window_size, 1, :discard)
    |> Enum.map(fn chunk -> Enum.sum(chunk) end)
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.count(fn [a, b] -> b > a end)
  end
end

Solver.main()
