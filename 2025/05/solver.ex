defmodule Solver.Y2025.D05 do
  def main() do
    [intervals, ingredients] = Reader.groups()
    intervals = Enum.map(intervals, &Interval.parse/1) |> Interval.join()
    ingredients = Enum.map(ingredients, &String.to_integer/1)
    Answer.part1(690, Enum.count(ingredients, &any?(intervals, &1)))
    Answer.part2(344_323_629_240_733, Enum.sum_by(intervals, &Interval.size/1))
  end

  @spec any?([Interval.t()], integer()) :: boolean()
  def any?(intervals, value) do
    Enum.any?(intervals, &Interval.in?(&1, value))
  end
end
