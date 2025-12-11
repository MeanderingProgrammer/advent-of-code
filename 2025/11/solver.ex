defmodule Graph do
  @type t :: %{String.t() => [String.t()]}

  @spec parse([String.t()]) :: t()
  def parse(lines) do
    Enum.flat_map(lines, fn line ->
      [input, outputs] = String.split(line, ": ")
      String.split(outputs) |> Enum.map(&{input, &1})
    end)
    |> Enum.reduce(%{}, fn {input, output}, acc ->
      Map.update(acc, output, [input], &[input | &1])
    end)
  end

  @spec num_paths(t(), [String.t()]) :: integer()
  def num_paths(graph, path) do
    path
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.map(fn [source, target] ->
      queue = :queue.from_list([target])
      Paths.sum(get_paths(graph, %{}, queue), source)
    end)
    |> Enum.product()
  end

  @spec get_paths(t(), Paths.t(), :queue.queue(String.t())) :: Paths.t()
  defp get_paths(graph, paths, queue) do
    case :queue.out(queue) do
      {:empty, _} ->
        paths

      {{:value, output}, queue} ->
        inputs = Map.get(graph, output, [])
        value = max(Paths.sum(paths, output), 1)

        {changes, paths} =
          Enum.map_reduce(inputs, paths, fn device, paths ->
            Paths.update(paths, device, output, value)
          end)

        outputs = if Enum.any?(changes), do: inputs, else: []
        queue = Enum.reduce(outputs, queue, &:queue.in/2)
        get_paths(graph, paths, queue)
    end
  end
end

defmodule Paths do
  @type t :: %{String.t() => %{String.t() => integer()}}

  @spec update(t(), String.t(), String.t(), integer()) :: {boolean(), t()}
  def update(paths, device, output, new) do
    outputs = Map.get(paths, device, %{})
    {old, outputs} = Map.get_and_update(outputs, output, &{&1, new})
    {old != new, Map.put(paths, device, outputs)}
  end

  @spec sum(t(), String.t()) :: integer()
  def sum(paths, device) do
    Map.get(paths, device, %{}) |> Map.values() |> Enum.sum()
  end
end

defmodule Solver.Y2025.D11 do
  def main() do
    graph = Reader.lines!() |> Graph.parse()
    part1 = Graph.num_paths(graph, ["you", "out"])
    paths1 = Graph.num_paths(graph, ["svr", "fft", "dac", "out"])
    paths2 = Graph.num_paths(graph, ["svr", "dac", "fft", "out"])
    Answer.part1!(749, part1)
    Answer.part2!(420_257_875_695_750, paths1 + paths2)
  end
end
