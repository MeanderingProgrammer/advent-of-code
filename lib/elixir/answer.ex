defmodule Answer do
  @spec timer((-> :ok)) :: :ok
  def timer(f) do
    start_time = System.monotonic_time(:nanosecond)
    f.()
    end_time = System.monotonic_time(:nanosecond)
    IO.puts("Runtime (ns): #{end_time - start_time}")
  end

  @spec part1(t, t) :: :ok when t: any()
  def part1(expected, actual), do: part(1, expected, actual)

  @spec part2(t, t) :: :ok when t: any()
  def part2(expected, actual), do: part(2, expected, actual)

  @spec part(1 | 2, t, t) :: :ok when t: any()
  defp part(n, expected, actual) do
    if expected == actual do
      IO.puts("Part #{n}: #{actual}")
    else
      raise RuntimeError, "Part #{n}: expected #{expected} got #{actual}"
    end
  end
end
