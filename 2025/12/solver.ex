defmodule Shape do
  @spec parse([String.t()]) :: integer()
  def parse(lines) do
    # 0:
    # ###
    # ##.
    # ##.
    {_, lines} = List.pop_at(lines, 0)

    lines
    |> Enum.join()
    |> String.graphemes()
    |> Enum.filter(&(&1 == "#"))
    |> Enum.count()
  end
end

defmodule Region do
  @type t :: {integer(), integer(), [integer()]}

  @spec parse(String.t()) :: t()
  def parse(s) do
    # 12x5: 1 0 1 0 3 2
    [dimensions, quantities] = String.split(s, ": ")
    [x, y] = String.split(dimensions, "x") |> Enum.map(&String.to_integer/1)
    quantities = String.split(quantities) |> Enum.map(&String.to_integer/1)
    {x, y, quantities}
  end

  @spec fits?(t(), [integer()]) :: boolean()
  def fits?({x, y, quantities}, shapes) do
    size =
      Enum.with_index(quantities)
      |> Enum.map(fn {quantity, i} -> quantity * Enum.at(shapes, i) end)
      |> Enum.sum()

    x * y > size
  end
end

defmodule Solver.Y2025.D12 do
  def main() do
    groups = Reader.groups!()
    {regions, shapes} = List.pop_at(groups, length(groups) - 1)
    shapes = Enum.map(shapes, &Shape.parse/1)
    regions = Enum.map(regions, &Region.parse/1)
    count = regions |> Enum.filter(&Region.fits?(&1, shapes)) |> Enum.count()
    Answer.part1!(406, count)
  end
end
