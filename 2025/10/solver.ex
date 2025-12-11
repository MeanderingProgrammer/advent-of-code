defmodule Machine do
  @type t :: {diagram(), csv(), [csv()]}
  @type diagram :: [boolean()]
  @type csv :: [integer()]

  @spec parse(String.t()) :: t()
  def parse(s) do
    # "[.#] (1) (1,2) (2) {1,2}"
    parts = String.split(s, " ")
    {diagram, parts} = List.pop_at(parts, 0)
    {joltage, buttons} = List.pop_at(parts, length(parts) - 1)

    # "[.#]" | [false, true]
    diagram =
      String.slice(diagram, 1..-2//1)
      |> String.graphemes()
      |> Enum.map(&(&1 == "#"))

    # {1,2} | [1, 2]
    joltage = csv(joltage)

    # ["(1)", "(1,2)", "(2)"] | [[1], [1, 2], [2]]
    buttons = Enum.map(buttons, &csv/1)

    {diagram, joltage, buttons}
  end

  @spec csv(String.t()) :: csv()
  defp csv(s) do
    # "(1,2)" | [1, 2]
    # "{1,2}" | [1, 2]
    String.slice(s, 1..-2//1)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  @spec start(t()) :: integer() | nil
  def start({diagram, _, buttons}) do
    Search.new(diagram, fn state ->
      Enum.map(buttons, fn button ->
        Enum.reduce(button, state, fn i, acc ->
          List.update_at(acc, i, &(!&1))
        end)
      end)
    end)
    |> Search.bfs(List.duplicate(false, length(diagram)))
  end

  @spec configure(t()) :: integer() | nil
  def configure({_, joltage, buttons}) do
    Search.new(joltage, fn state ->
      Enum.map(buttons, fn button ->
        Enum.reduce(button, state, fn i, acc ->
          List.update_at(acc, i, &(&1 + 1))
        end)
      end)
      |> Enum.filter(fn state ->
        Enum.zip(state, joltage) |> Enum.all?(fn {a, b} -> a <= b end)
      end)
    end)
    |> Search.bfs(List.duplicate(0, length(joltage)))
  end
end

defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    machines = Reader.lines() |> Enum.map(&Machine.parse/1)
    Answer.part1(522, Enum.sum_by(machines, &Machine.start/1))
    # part 2 too slow with search, need some linear solver
    # Answer.part2(18105, Enum.sum_by(machines, &Machine.configure/1))
    Answer.part2("DNF", "DNF")
  end
end

Solver.main()
