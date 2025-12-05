defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    [intervals, ingredients] = Reader.groups()
    intervals = intervals |> Enum.map(&Interval.parse/1) |> combine()
    ingredients = ingredients |> Enum.map(&String.to_integer/1)
    Answer.part1(690, ingredients |> Enum.count(&any?(intervals, &1)))
    Answer.part2(344_323_629_240_733, intervals |> Enum.map(&Interval.size(&1)) |> Enum.sum())
  end

  @spec combine([Interval.t()]) :: [Interval.t()]
  def combine(intervals) do
    intervals
    |> Enum.sort_by(&elem(&1, 0))
    |> Enum.reduce([], fn {cs, ce}, acc ->
      case acc do
        [] ->
          [{cs, ce}]

        [{ps, pe} | rest] ->
          if cs <= pe do
            [{ps, max(pe, ce)} | rest]
          else
            [{cs, ce}, {ps, pe} | rest]
          end
      end
    end)
  end

  @spec any?([Interval.t()], integer()) :: boolean()
  def any?(intervals, value) do
    intervals |> Enum.any?(&Interval.in?(&1, value))
  end
end

Solver.main()
