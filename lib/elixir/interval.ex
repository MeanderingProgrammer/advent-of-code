defmodule Interval do
  @type t :: {integer(), integer()}

  @spec parse(String.t()) :: t()
  def parse(s) do
    String.split(s, "-")
    |> Enum.map(&String.to_integer/1)
    |> List.to_tuple()
  end

  @spec valid?(t()) :: boolean()
  def valid?({s, e}), do: s <= e

  @spec size(t()) :: integer()
  def size({s, e}), do: e - s + 1

  @spec in?(t(), integer()) :: boolean()
  def in?({s, e}, v), do: v >= s && v <= e

  @spec overlaps?(t(), t()) :: boolean()
  def overlaps?({s1, e1}, {s2, e2}), do: max(s1, s2) <= min(e1, e2)

  @spec merge(t(), t()) :: t() | nil
  def merge({s1, e1} = a, {s2, e2} = b) do
    if overlaps?(a, b), do: {min(s1, s2), max(e1, e2)}, else: nil
  end

  @spec join([t()]) :: [t()]
  def join(intervals) do
    intervals
    |> Enum.sort_by(&elem(&1, 0))
    |> Enum.reduce([], fn
      n, [] ->
        [n]

      n, [p | rest] ->
        case merge(p, n) do
          nil -> [n, p | rest]
          interval -> [interval | rest]
        end
    end)
  end
end
