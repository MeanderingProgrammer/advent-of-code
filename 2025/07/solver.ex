defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    grid = Reader.lines() |> Grid.parse(["."])

    %Point{x: x, y: y0} = Grid.values(grid, "S") |> List.first()
    {_, {_, y1}} = Grid.bounds(grid)

    {splits, timelines} =
      Enum.map_reduce((y0 + 1)..y1, %{x => 1}, fn y, acc ->
        branches =
          Enum.flat_map(acc, fn {x, n} ->
            if Map.has_key?(grid, %Point{x: x, y: y}) do
              [{x - 1, n}, {x + 1, n}]
            else
              [{x, n}]
            end
          end)

        splits = length(branches) - map_size(acc)

        timelines =
          Enum.reduce(branches, %{}, fn {k, v}, acc ->
            Map.update(acc, k, v, &(&1 + v))
          end)

        {splits, timelines}
      end)

    Answer.part1(1649, Enum.sum(splits))
    Answer.part2(16_937_871_060_075, Enum.sum(Map.values(timelines)))
  end
end

Solver.main()
