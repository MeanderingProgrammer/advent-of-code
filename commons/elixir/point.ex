defmodule Point do
  @enforce_keys [:x, :y]
  defstruct [:x, :y]

  @type t :: %__MODULE__{x: integer(), y: integer()}

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
