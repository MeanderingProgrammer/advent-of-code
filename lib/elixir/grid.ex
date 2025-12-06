defmodule Grid do
  @type t :: %{Point.t() => String.t()}

  @spec parse([String.t()], [String.t()]) :: t()
  def parse(lines, ignore) do
    for {line, y} <- lines |> Enum.with_index(),
        {value, x} <- line |> String.graphemes() |> Enum.with_index(),
        value not in ignore,
        into: %{},
        do: {%Point{x: x, y: y}, value}
  end
end
