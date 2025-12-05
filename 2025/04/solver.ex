defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    grid = Reader.lines() |> Grid.parse(["."])
    removed = cleanup(grid)
    Answer.part1(1464, Enum.at(removed, 0))
    Answer.part2(8409, Enum.sum(removed))
  end

  @spec cleanup(Grid.t()) :: [integer()]
  def cleanup(grid) do
    case step(grid) do
      [] -> []
      points -> [length(points) | cleanup(Map.drop(grid, points))]
    end
  end

  @spec step(Grid.t()) :: [Point.t()]
  def step(grid) do
    grid
    |> Map.keys()
    |> Enum.filter(&accessible?(grid, &1))
  end

  @spec accessible?(Grid.t(), Point.t()) :: boolean()
  def accessible?(grid, point) do
    point
    |> Point.all_neighbors()
    |> Enum.count(&Map.has_key?(grid, &1)) < 4
  end
end

Solver.main()
