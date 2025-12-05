defmodule Grid do
  def parse(lines) do
    for {line, y} <- lines |> Enum.with_index(),
        {value, x} <- line |> String.graphemes() |> Enum.with_index(),
        into: %{},
        do: {%Point{x: x, y: y}, value}
  end
end
