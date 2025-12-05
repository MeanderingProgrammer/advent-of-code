defmodule Solver do
  def main do
    Answer.timer(&solution/0)
  end

  def solution do
    lines = Reader.lines()
    grid = lines |> Grid.parse()
    removed = cleanup(grid)
    Answer.part1(1464, Enum.at(removed, 0))
    Answer.part2(8409, Enum.sum(removed))
  end

  def cleanup(grid) do
    case step(grid) do
      [] -> []
      points -> [length(points) | cleanup(Map.drop(grid, points))]
    end
  end

  def step(grid) do
    grid
    |> Map.keys()
    |> Enum.filter(&roll?(grid, &1))
    |> Enum.filter(&accessible?(grid, &1))
  end

  def accessible?(grid, point) do
    Point.all_neighbors(point) |> Enum.count(&roll?(grid, &1)) < 4
  end

  def roll?(grid, point) do
    Map.get(grid, point) == "@"
  end
end

Solver.main()
