defmodule Point do
  @enforce_keys [:x, :y]
  defstruct [:x, :y]

  @type t :: %__MODULE__{x: integer(), y: integer()}

  @spec parse(String.t()) :: t()
  def parse(string) do
    [x, y] = String.split(string, ",") |> Enum.map(&String.to_integer/1)
    %Point{x: x, y: y}
  end

  @spec neighbors(t()) :: [t()]
  def neighbors(%Point{x: x, y: y}) do
    [
      %Point{x: x + 1, y: y},
      %Point{x: x - 1, y: y},
      %Point{x: x, y: y + 1},
      %Point{x: x, y: y - 1}
    ]
  end

  @spec all_neighbors(t()) :: [t()]
  def all_neighbors(%Point{x: x, y: y}) do
    [
      %Point{x: x + 1, y: y + 1},
      %Point{x: x + 1, y: y - 1},
      %Point{x: x - 1, y: y + 1},
      %Point{x: x - 1, y: y - 1}
    ] ++ neighbors(%Point{x: x, y: y})
  end
end

defmodule Point3d do
  @enforce_keys [:x, :y, :z]
  defstruct [:x, :y, :z]

  @type t :: %__MODULE__{x: integer(), y: integer(), z: integer()}

  @spec parse(String.t()) :: t()
  def parse(string) do
    [x, y, z] = String.split(string, ",") |> Enum.map(&String.to_integer/1)
    %Point3d{x: x, y: y, z: z}
  end

  @spec euclidean(t(), t()) :: float()
  def euclidean(p1, p2) do
    Enum.zip(to_list(p1), to_list(p2))
    |> Enum.map(&(elem(&1, 0) - elem(&1, 1)))
    |> Enum.map(&:math.pow(&1, 2))
    |> Enum.sum()
    |> :math.sqrt()
  end

  @spec to_list(t()) :: [integer()]
  defp to_list(%Point3d{x: x, y: y, z: z}) do
    [x, y, z]
  end
end
