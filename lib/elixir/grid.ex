defmodule Grid do
  @type t :: %{Point.t() => String.t()}

  @spec parse([String.t()], [String.t()]) :: t()
  def parse(lines, ignore) do
    for {line, y} <- Enum.with_index(lines),
        {value, x} <- Enum.with_index(String.graphemes(line)),
        value not in ignore,
        into: %{},
        do: {%Point{x: x, y: y}, value}
  end

  @spec values(t(), String.t()) :: [Point.t()]
  def values(grid, value) do
    grid |> Map.filter(&(elem(&1, 1) == value)) |> Map.keys()
  end

  @spec bounds(t()) :: {Interval.t(), Interval.t()}
  def bounds(grid) do
    points = Map.keys(grid)
    xs = Enum.map(points, & &1.x)
    ys = Enum.map(points, & &1.y)
    {Enum.min_max(xs), Enum.min_max(ys)}
  end

  @spec to_string(t()) :: String.t()
  def to_string(grid) do
    {{min_x, max_x}, {min_y, max_y}} = bounds(grid)

    Enum.map_join(min_y..max_y, "\n", fn y ->
      Enum.map_join(min_x..max_x, "", fn x ->
        Map.get(grid, %Point{x: x, y: y}, ".")
      end)
    end)
  end
end
