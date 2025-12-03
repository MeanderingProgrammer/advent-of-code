defmodule Answer do
  def timer(f) do
    start_time = System.monotonic_time(:nanosecond)
    f.()
    end_time = System.monotonic_time(:nanosecond)
    IO.puts("Runtime (ns): #{end_time - start_time}")
  end

  def part1(expected, actual) do
    part(1, expected, actual)
  end

  def part2(expected, actual) do
    part(2, expected, actual)
  end

  defp part(n, expected, actual) do
    if expected == actual do
      IO.puts("Part #{n}: #{actual}")
    else
      raise RuntimeError, "Part #{n}: expected #{expected} found #{actual}"
    end
  end
end
