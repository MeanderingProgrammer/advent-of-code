defmodule Answer do
  @spec part1!(t, t) :: :ok when t: any()
  def part1!(expected, actual), do: part!(1, expected, actual)

  @spec part2!(t, t) :: :ok when t: any()
  def part2!(expected, actual), do: part!(2, expected, actual)

  @spec part!(1 | 2, t, t) :: :ok when t: any()
  defp part!(n, expected, actual) do
    if expected == actual do
      IO.puts("Part #{n}: #{actual}")
    else
      raise "Part #{n}: expected #{expected} got #{actual}"
    end
  end
end
