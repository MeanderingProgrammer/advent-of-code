defmodule Solver do
  def main do
    Answer.timer(&solution/0)
  end

  def solution do
    data = Reader.text()
    IO.inspect(data)
    Answer.part1(1, 1)
    Answer.part2(1, 1)
  end
end

Solver.main()
