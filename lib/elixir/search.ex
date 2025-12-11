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
  def bfs(search, start) do
    run(search, [{0, start}])
  end

  @spec run(t(v), [{integer(), v}]) :: integer() | nil when v: any()
  defp run(search, queue) do
    case queue do
      [] ->
        nil

      [{n, state} | queue] ->
        cond do
          state === search.target ->
            n

          true ->
            seen = MapSet.put(search.seen, state)

            next =
              search.neighbors.(state)
              |> Enum.filter(fn state -> not MapSet.member?(seen, state) end)
              |> Enum.map(&{n + 1, &1})

            seen =
              Enum.reduce(next, seen, fn {_, state}, acc ->
                MapSet.put(acc, state)
              end)

            run(%{search | seen: seen}, queue ++ next)
        end
    end
  end
end
