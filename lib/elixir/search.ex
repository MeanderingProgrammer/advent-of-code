defmodule Search do
  @enforce_keys [:target, :neighbors, :seen]
  defstruct [:target, :neighbors, :seen]

  @opaque t(v) :: %__MODULE__{target: v, neighbors: (v -> [v]), seen: MapSet.t(v)}

  @spec new(v, (v -> [v])) :: t(v) when v: any()
  def new(target, neighbors) do
    %Search{target: target, neighbors: neighbors, seen: MapSet.new()}
  end

  @spec bfs(t(v), v) :: integer() when v: any()
  def bfs(search, start) do
    run(search, [{start, 0}])
  end

  @spec run(t(v), [{v, integer()}]) :: integer() when v: any()
  defp run(search, queue) do
    case queue do
      [{state, n} | queue] ->
        cond do
          state === search.target ->
            n

          true ->
            seen = MapSet.put(search.seen, state)

            next =
              search.neighbors.(state)
              |> Enum.filter(fn state -> not MapSet.member?(seen, state) end)
              |> Enum.map(&{&1, n + 1})

            seen =
              Enum.reduce(next, seen, fn {state, _}, acc ->
                MapSet.put(acc, state)
              end)

            run(%{search | seen: seen}, queue ++ next)
        end

      _ ->
        -1
    end
  end
end
