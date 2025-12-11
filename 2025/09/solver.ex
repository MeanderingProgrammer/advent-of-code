defmodule Rectangle do
  @enforce_keys [:x, :y]
  defstruct [:x, :y]

  @type t :: %__MODULE__{x: Interval.t(), y: Interval.t()}

  @spec new({Point.t(), Point.t()}) :: t()
  def new({a, b}) do
    %Rectangle{
      x: {min(a.x, b.x), max(a.x, b.x)},
      y: {min(a.y, b.y), max(a.y, b.y)}
    }
  end

  @spec area(t()) :: integer()
  def area(%Rectangle{x: x, y: y}) do
    Interval.size(x) * Interval.size(y)
  end

  @spec inner(t()) :: t() | nil
  def inner(%Rectangle{x: {xs, xe}, y: {ys, ye}}) do
    x = {xs + 1, xe - 1}
    y = {ys + 1, ye - 1}
    valid = Interval.valid?(x) && Interval.valid?(y)
    if valid, do: %Rectangle{x: x, y: y}, else: nil
  end

  @spec overlaps?(t(), t()) :: boolean()
  def overlaps?(%Rectangle{x: x1, y: y1}, %Rectangle{x: x2, y: y2}) do
    Interval.overlaps?(x1, x2) && Interval.overlaps?(y1, y2)
  end
end

defmodule Polygon do
  @type t :: [Rectangle.t()]

  @spec new([Point.t()]) :: t()
  def new(points) do
    points
    |> Enum.with_index()
    |> Enum.map(fn {a, i} ->
      j = if i == 0, do: length(points) - 1, else: i - 1
      Rectangle.new({a, Enum.at(points, j)})
    end)
  end

  @spec contains?(t(), Rectangle.t()) :: boolean()
  def contains?(polygon, rectangle) do
    case Rectangle.inner(rectangle) do
      nil -> false
      inner -> !Enum.any?(polygon, &Rectangle.overlaps?(&1, inner))
    end
  end
end

defmodule Solver.Y2025.D09 do
  def main() do
    points = Reader.lines!() |> Enum.map(&Point.parse/1)
    polygon = Polygon.new(points)
    Answer.part1!(4_759_420_470, max_area(points, polygon, false))
    Answer.part2!(1_603_439_684, max_area(points, polygon, true))
  end

  @spec max_area([Point.t()], Polygon.t(), boolean()) :: integer()
  def max_area(points, polygon, check) do
    n = length(points)

    0..(n - 2)
    |> Enum.flat_map(fn i -> Enum.map((i + 1)..(n - 1), &{i, &1}) end)
    |> Enum.map(fn {a, b} -> {Enum.at(points, a), Enum.at(points, b)} end)
    |> Enum.map(&Rectangle.new/1)
    |> Enum.filter(&(!check || Polygon.contains?(polygon, &1)))
    |> Enum.map(&Rectangle.area/1)
    |> Enum.max()
  end
end
