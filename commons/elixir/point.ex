defmodule Point do
  defstruct [:x, :y]

  def all_neighbors(%Point{x: x, y: y}) do
    [
      %Point{x: x + 1, y: y},
      %Point{x: x - 1, y: y},
      %Point{x: x, y: y + 1},
      %Point{x: x, y: y - 1},
      %Point{x: x + 1, y: y + 1},
      %Point{x: x + 1, y: y - 1},
      %Point{x: x - 1, y: y + 1},
      %Point{x: x - 1, y: y - 1}
    ]
  end
end
