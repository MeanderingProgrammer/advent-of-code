open Core

let modulo (x : int) (y : int) : int =
  let result = x mod y in
  if result >= 0 then result else result + y

let valid_neighbor (grid : Aoc.Grid.t) (len : int) (p : Aoc.Point.t) : bool =
  let x, y = (modulo p.x len, modulo p.y len) in
  let ch = Hashtbl.find_exn grid { x; y } in
  not (Char.equal '#' ch)

let get_neighbors (grid : Aoc.Grid.t) (len : int) (p : Aoc.Point.t) =
  let _, neighbors = List.unzip (Aoc.Point.adjacent p) in
  let neighbors = List.filter ~f:(valid_neighbor grid len) neighbors in
  Aoc.Types.PointSet.of_list neighbors

let step (grid : Aoc.Grid.t) (len : int) current =
  Set.fold ~init:Aoc.Types.PointSet.empty
    ~f:(fun acc x -> Set.union acc (get_neighbors grid len x))
    current

let rec step_n (grid : Aoc.Grid.t) (len : int) (n : int) current =
  match Int.equal n 0 with
  | true -> (Set.length current, current)
  | false -> step_n grid len (n - 1) (step grid len current)

let part2_magic (a0 : int) (a1 : int) (a2 : int) (n : int) : int =
  let b0 = a0 in
  let b1 = a1 - a0 in
  let b2 = a2 - a1 - b1 in
  b0 + (b1 * n) + (n * (n - 1) / 2 * b2)

let () =
  let grid = Aoc.Reader.read_grid () in
  let len = (Aoc.Grid.max grid).x + 1 in

  let start = Aoc.Grid.find_value grid 'S' in
  let initial = Aoc.Types.PointSet.of_list [ start ] in
  let part1, points = step_n grid len 64 initial in

  (* Honestly no clue, something about patterns in a growing diamond shape *)
  (* https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7 *)
  let a0, points = step_n grid len 1 points in
  let a1, points = step_n grid len len points in
  let a2, _ = step_n grid len len points in
  let iterations = 26501365 / len in
  let part2 = part2_magic a0 a1 a2 iterations in

  Aoc.Answer.part1 3847 part1 string_of_int;
  Aoc.Answer.part2 637537341306357 part2 string_of_int
