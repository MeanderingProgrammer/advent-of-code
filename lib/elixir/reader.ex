defmodule Reader do
  @spec text() :: String.t()
  def text() do
    get_filepath() |> File.read!() |> String.trim("\n")
  end

  @spec lines() :: [String.t()]
  def lines() do
    text() |> String.split("\n")
  end

  @spec groups() :: [[String.t()]]
  def groups() do
    text() |> String.split("\n\n") |> Enum.map(&String.split(&1, "\n"))
  end

  @spec get_filepath() :: Path.t()
  defp get_filepath() do
    {:current_stacktrace, frames} = Process.info(self(), :current_stacktrace)

    [year, day, _] =
      frames
      |> Enum.map(&elem(&1, 3)[:file])
      |> Enum.find(&(Path.basename(&1) == "solver.ex"))
      |> Path.split()

    test? = Enum.member?(System.argv(), "--test")
    file = if test?, do: "sample.txt", else: "data.txt"

    Path.join(["data", year, day, file])
  end
end
