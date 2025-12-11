defmodule Search do
  @enforce_keys [:target, :neighbors, :seen]
  defstruct [:target, :neighbors, :seen]

  @opaque t(v) :: %__MODULE__{target: v, neighbors: (v -> [v]), seen: MapSet.t(v)}

  @spec new(v, (v -> [v])) :: t(v) when v: any()
  def new(target, neighbors) do
    %Search{
      target: target,
      neighbors: neighbors,
      seen: MapSet.new()
    }
  end

  @spec bfs(t(v), v) :: integer() | nil when v: any()
  def bfs(search, source), do: run(search, :queue.from_list([{0, source}]))

  @spec run(t(v), :queue.queue({integer(), v})) :: integer() | nil when v: any()
  defp run(search, queue) do
    case :queue.out(queue) do
      {:empty, _} ->
        nil

      {{:value, {n, state}}, queue} ->
        cond do
          state == search.target ->
            n

          true ->
            seen = MapSet.put(search.seen, state)
            neighbors = search.neighbors.(state)
            next = Enum.filter(neighbors, &(not MapSet.member?(seen, &1)))
            seen = Enum.reduce(next, seen, &MapSet.put(&2, &1))
            queue = Enum.reduce(next, queue, &:queue.in({n + 1, &1}, &2))
            run(%{search | seen: seen}, queue)
        end
    end
  end
end
