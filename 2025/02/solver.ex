defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    values = Reader.text() |> String.split(",") |> Enum.map(&Interval.parse/1)

    {part1, part2} =
      values
      |> Task.async_stream(&longest_prefixes/1, ordered: false)
      |> Enum.reduce({0, 0}, fn {:ok, {p1, p2}}, {a1, a2} -> {a1 + p1, a2 + p2} end)

    Answer.part1(23_701_357_374, part1)
    Answer.part2(34_284_458_938, part2)
  end

  @spec longest_prefixes(Interval.t()) :: {integer(), integer()}
  def longest_prefixes({s, e}) do
    Enum.reduce(s..e, {0, 0}, fn i, {a1, a2} ->
      digits = Integer.digits(i)
      half = div(length(digits) + 1, 2)

      case longest_prefix(digits) do
        0 -> {a1, a2}
        ^half -> {a1 + i, a2 + i}
        _ -> {a1, a2 + i}
      end
    end)
  end

  @spec longest_prefix([integer()]) :: integer()
  def longest_prefix(digits) do
    div(length(digits), 2)..1//-1
    |> Enum.find(0, &is_prefix?(digits, &1))
  end

  @spec is_prefix?([integer()], integer()) :: boolean()
  def is_prefix?(digits, size) do
    case rem(length(digits), size) do
      0 ->
        prefix = Enum.slice(digits, 0, size)

        size..(length(digits) - size)//size
        |> Enum.all?(&(Enum.slice(digits, &1, size) == prefix))

      _ ->
        false
    end
  end
end

Solver.main()
