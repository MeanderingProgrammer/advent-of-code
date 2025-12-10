defmodule Interval do
  @type t :: {integer(), integer()}

  @spec parse(String.t()) :: t()
  def parse(string) do
    [s, e] = String.split(string, "-")
    {String.to_integer(s), String.to_integer(e)}
  end

  @spec size(t()) :: integer()
  def size({s, e}) do
    e - s + 1
  end

  @spec in?(t(), integer()) :: boolean()
  def in?({s, e}, value) do
    value >= s && value <= e
  end

  @spec overlaps?(t(), t()) :: boolean()
  def overlaps?({s1, e1}, {s2, e2}) do
    max(s1, s2) <= min(e1, e2)
  end
end
