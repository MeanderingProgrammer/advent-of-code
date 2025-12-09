defmodule Solver do
  def main() do
    Answer.timer(&solution/0)
  end

  def solution() do
    points = Reader.lines() |> Enum.map(&Point3d.parse/1)

    n = length(points)
    parents = Enum.to_list(0..(n - 1))
    ranks = List.duplicate(1, n)

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
      |> Enum.reduce_while({{parents, ranks}, nil}, fn {edge, i}, {acc, nth} ->
        {parents, ranks} = union(acc, edge)
        nth = if i == 999, do: ranks, else: nth

        if Enum.max(ranks) == n do
          {:halt, {nth, edge}}
        else
          {:cont, {{parents, ranks}, nth}}
        end
      end)

    part1 =
      nth
      |> Enum.sort()
      |> Enum.reverse()
      |> Enum.take(3)
      |> Enum.product()

    part2 =
      last
      |> Tuple.to_list()
      |> Enum.map(&Enum.at(points, &1).x)
      |> Enum.product()

    Answer.part1(181_584, part1)
    Answer.part2(8_465_902_405, part2)
  end

  @spec union({[integer()], [integer()]}, {integer(), integer()}) :: {[integer()], [integer()]}
  def union({parents, ranks}, {n1, n2}) do
    {p1, p2} = {find(parents, n1), find(parents, n2)}

    if p1 == p2 do
      {parents, ranks}
    else
      {r1, r2} = {Enum.at(ranks, p1), Enum.at(ranks, p2)}
      {parent, child} = if r1 >= r2, do: {p1, p2}, else: {p2, p1}
      parents = List.replace_at(parents, child, parent)
      ranks = List.update_at(ranks, parent, &(&1 + Enum.at(ranks, child)))
      ranks = List.replace_at(ranks, child, 0)
      {parents, ranks}
    end
  end

  @spec find([integer()], integer()) :: integer()
  def find(parents, node) do
    case Enum.at(parents, node) do
      ^node -> node
      node -> find(parents, node)
    end
  end
end

Solver.main()
