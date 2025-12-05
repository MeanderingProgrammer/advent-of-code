defmodule Reader do
  @spec text() :: String.t()
  def text() do
    get_filepath() |> File.read!() |> String.trim()
  end

  @spec lines() :: [String.t()]
  def lines() do
    text() |> String.split("\n")
  end

  @spec get_filepath() :: Path.t()
  defp get_filepath() do
    {:current_stacktrace, frames} = Process.info(self(), :current_stacktrace)

    [year, day, _] =
      frames
      |> Enum.map(fn {_, _, _, meta} -> meta[:file] end)
      |> Enum.find(fn path -> Path.basename(path) == "solver.ex" end)
      |> Path.split()

    test? = Enum.member?(System.argv(), "--test")
    file = if test?, do: "sample.txt", else: "data.txt"

    Path.join(["data", year, day, file])
  end
end
