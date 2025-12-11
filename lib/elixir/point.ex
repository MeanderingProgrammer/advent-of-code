defmodule Point do
  @enforce_keys [:x, :y]
  defstruct [:x, :y]

  @type t :: %__MODULE__{x: integer(), y: integer()}

  @cardinals [{1, 0}, {-1, 0}, {0, 1}, {0, -1}]
  @diagonals [{1, 1}, {1, -1}, {-1, 1}, {-1, -1}]

  @spec parse(String.t()) :: t()
  def parse(s) do
    String.split(s, ",")
    |> Enum.map(&String.to_integer/1)
    |> then(fn [x, y] -> %Point{x: x, y: y} end)
  end

  @spec add(t(), {integer(), integer()}) :: t()
  def add(%Point{x: x, y: y}, {dx, dy}) do
    %Point{x: x + dx, y: y + dy}
  end

  @spec neighbors(t()) :: [t()]
  def neighbors(p) do
    Enum.map(@cardinals, &add(p, &1))
  end

  @spec all_neighbors(t()) :: [t()]
  def all_neighbors(p) do
    Enum.map(@diagonals, &add(p, &1)) ++ neighbors(p)
  end
end

defmodule Point3d do
  @enforce_keys [:x, :y, :z]
  defstruct [:x, :y, :z]

  @type t :: %__MODULE__{x: integer(), y: integer(), z: integer()}

  @spec parse(String.t()) :: t()
  def parse(s) do
    String.split(s, ",")
    |> Enum.map(&String.to_integer/1)
    |> then(fn [x, y, z] -> %Point3d{x: x, y: y, z: z} end)
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
