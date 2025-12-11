defmodule Dial do
  defstruct value: 50, size: 100

  @type t :: %__MODULE__{value: integer(), size: integer()}

  @spec move(t(), boolean(), integer()) :: {t(), integer()}
  def move(%Dial{} = dial, right, amount) do
    # simplify full rotations
    clicks = div(amount, dial.size)
    amount = rem(amount, dial.size)

    {value, rollover} =
      if right do
        rollover = dial.value + amount >= dial.size
        value = dial.value + amount
        value = if value >= dial.size, do: value - dial.size, else: value
        {value, rollover}
      else
        rollover = dial.value > 0 and dial.value <= amount
        value = dial.value - amount
        value = if value < 0, do: value + dial.size, else: value
        {value, rollover}
      end

    clicks = if rollover, do: clicks + 1, else: clicks
    {%{dial | value: value}, clicks}
  end
end

defmodule Solver.Y2025.D01 do
  def main() do
    lines = Reader.lines!()

    {_, zeros, clicks} =
      Enum.reduce(lines, {%Dial{}, 0, 0}, fn line, {dial, zeros, clicks} ->
        right = String.starts_with?(line, "R")
        amount = String.to_integer(String.slice(line, 1..-1//1))
        {dial, more_clicks} = Dial.move(dial, right, amount)
        more_zeros = if dial.value == 0, do: 1, else: 0
        {dial, zeros + more_zeros, clicks + more_clicks}
      end)

    Answer.part1!(1120, zeros)
    Answer.part2!(6554, clicks)
  end
end
