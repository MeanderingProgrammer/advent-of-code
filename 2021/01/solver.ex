defmodule Solver.Y2021.D01 do
  def main() do
    values = Reader.lines!() |> Enum.map(&String.to_integer/1)
    Answer.part1!(1292, increases(values, 1))
    Answer.part2!(1262, increases(values, 3))
  end

  @spec increases([integer()], pos_integer()) :: integer()
  def increases(values, n) do
    values
    |> Enum.chunk_every(n, 1, :discard)
    |> Enum.map(&Enum.sum(&1))
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.count(fn [a, b] -> b > a end)
  end
end
