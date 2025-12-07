defmodule Problems do
  @type t :: [problem()]
  @type problem :: {[String.t()], op()}
  @type op :: ([integer()] -> integer())
  @type parser :: ([String.t()] -> [integer()])

  @spec parse([String.t()]) :: t()
  def parse(lines) do
    # "123 328  51 64  " | {["123 ", " 45 ", "  6 "], Enum.product}
    # " 45 64  387 23  " | {["328 ", "64  ", "98  "], Enum.sum}
    # "  6 98  215 3145" | {[" 51 ", "387 ", "215 "], Enum.product}
    # "*   +   *   +   " | {["64  ", "23  ", "3145"], Enum.sum}
    {ops, values} = List.pop_at(lines, length(lines) - 1)
    ops = Regex.scan(~r/\S\s+/, ops) |> List.flatten()
    values = Enum.map(values, &chunks(ops, &1))

    Enum.zip(
      values
      |> Enum.zip()
      |> Enum.map(&Tuple.to_list/1),
      ops
      |> Enum.map(&String.trim/1)
      |> Enum.map(fn
        "+" -> &Enum.sum/1
        "*" -> &Enum.product/1
      end)
    )
  end

  @spec chunks([String.t()], String.t()) :: [String.t()]
  defp chunks(ops, line) do
    ops
    |> Enum.map(&String.length/1)
    |> Enum.map_reduce(line, &String.split_at(&2, &1))
    |> elem(0)
  end

  @spec solve(t(), parser()) :: integer()
  def solve(problems, parser) do
    problems
    |> Enum.map(fn {values, op} -> values |> parser.() |> op.() end)
    |> Enum.sum()
  end
end

defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    problems = Reader.lines() |> Problems.parse()

    Answer.part1(
      7_229_350_537_438,
      Problems.solve(problems, fn values ->
        Enum.map(values, &(&1 |> String.trim() |> String.to_integer()))
      end)
    )

    Answer.part2(
      11_479_269_003_550,
      Problems.solve(problems, fn values ->
        values
        |> Enum.map(&String.graphemes/1)
        |> Enum.zip()
        |> Enum.map(&(&1 |> Tuple.to_list() |> Enum.join() |> String.trim()))
        |> Enum.filter(&(String.length(&1) > 0))
        |> Enum.map(&String.to_integer/1)
      end)
    )
  end
end

Solver.main()
