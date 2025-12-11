defmodule UnionFind do
  @enforce_keys [:parents, :ranks]
  defstruct [:parents, :ranks]

  @type t :: %__MODULE__{parents: [integer()], ranks: [integer()]}

  @spec new(integer()) :: t()
  def new(n) do
    %UnionFind{
      parents: Enum.to_list(0..(n - 1)),
      ranks: List.duplicate(1, n)
    }
  end

  @spec union(t(), {integer(), integer()}) :: t()
  def union(%UnionFind{parents: parents, ranks: ranks} = uf, {n1, n2}) do
    {p1, p2} = {find(parents, n1), find(parents, n2)}

    if p1 == p2 do
      uf
    else
      {r1, r2} = {Enum.at(ranks, p1), Enum.at(ranks, p2)}
      {parent, child} = if r1 >= r2, do: {p1, p2}, else: {p2, p1}
      parents = List.replace_at(parents, child, parent)
      ranks = List.update_at(ranks, parent, &(&1 + Enum.at(ranks, child)))
      ranks = List.replace_at(ranks, child, 0)
      %UnionFind{parents: parents, ranks: ranks}
    end
  end

  @spec find([integer()], integer()) :: integer()
  defp find(parents, node) do
    case Enum.at(parents, node) do
      ^node -> node
      node -> find(parents, node)
    end
  end
end

defmodule Solver.Y2025.D08 do
  def main() do
    points = Reader.lines() |> Enum.map(&Point3d.parse/1)

    n = length(points)
    circuit = UnionFind.new(n)

    edges =
      points
      |> Enum.with_index()
      |> Enum.flat_map(fn {p1, i1} ->
        points
        |> Enum.with_index()
        |> Enum.drop(i1 + 1)
        |> Enum.map(fn {p2, i2} -> {i1, i2, Point3d.euclidean(p1, p2)} end)
      end)
      |> Enum.sort_by(fn {_, _, distance} -> distance end)
      |> Enum.map(fn {n1, n2, _} -> {n1, n2} end)

    {nth, last} =
      Enum.with_index(edges)
      |> Enum.reduce_while({circuit, nil}, fn {edge, i}, {acc, nth} ->
        acc = UnionFind.union(acc, edge)
        nth = if i == 999, do: acc.ranks, else: nth

        if Enum.max(acc.ranks) == n do
          {:halt, {nth, edge}}
        else
          {:cont, {acc, nth}}
        end
      end)

    ranks = nth |> Enum.sort() |> Enum.reverse()
    xs = last |> Tuple.to_list() |> Enum.map(&Enum.at(points, &1).x)

    Answer.part1(181_584, Enum.product(Enum.take(ranks, 3)))
    Answer.part2(8_465_902_405, Enum.product(xs))
  end
end
