open Aoc
open Core

let modulo (x : int) (y : int) : int =
  let result = x mod y in
  if result >= 0 then result else result + y

let valid_neighbor (grid : Grid.t) (len : int) (p : Point.t) : bool =
  let x, y = (modulo p.x len, modulo p.y len) in
  let ch = Hashtbl.find_exn grid { x; y } in
  not (Char.equal '#' ch)

let get_neighbors (grid : Grid.t) (len : int) (p : Point.t) =
  let _, neighbors = List.unzip (Point.adjacent p) in
  let neighbors = List.filter ~f:(valid_neighbor grid len) neighbors in
  Types.PointSet.of_list neighbors

let step (grid : Grid.t) (len : int) (current : Types.PointSet.t) :
    Types.PointSet.t =
  Set.fold ~init:Types.PointSet.empty
    ~f:(fun acc x -> Set.union acc (get_neighbors grid len x))
    current

let rec step_n (grid : Grid.t) (len : int) (n : int)
    (current : Types.PointSet.t) : int * Types.PointSet.t =
  match Int.equal n 0 with
  | true -> (Set.length current, current)
  | false -> step_n grid len (n - 1) (step grid len current)

let solve_quadratic (f : int array) (n : int) : int =
  (* f(x) = ax² + bx + c = plots in 65 + 131 * x *)
  (* Solving for c is easy since we have f[0] *)
  (* f[0] = a(0)² + b(0) + c -> c = f[0] *)
  (* Solve for b in terms of a using f[1] & c = f[0] *)
  (* f[1] = a(1)² + b(1) + f[0] *)
  (* b = f[1] - f[0] - a *)
  (* Solve for a using f[2], b, & c = f[0] *)
  (* f[2] = a(2)² + b(2) + f[0] *)
  (* 4a + 2b = f[2] - f[0] *)
  (* 4a + 2(f[1] - f[0] - a) = f[2] - f[0] *)
  (* 4a + 2f[1] - 2f[0] - 2a = f[2] - f[0] *)
  (* a = (f[2] - 2f[1] + f[0]) / 2 *)
  let a = (f.(2) - (2 * f.(1)) + f.(0)) / 2 in
  let b = f.(1) - f.(0) - a in
  let c = f.(0) in
  (a * n * n) + (b * n) + c

let solution () =
  let grid = Reader.read_grid () in
  let len = (Grid.max grid).x + 1 in

  let start = Grid.find_value grid 'S' in
  let initial = Types.PointSet.of_list [ start ] in
  let part1, points = step_n grid len 64 initial in

  (* Quadratic pattern in a growing diamond shape *)
  (* https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7 *)
  let f0, points = step_n grid len 1 points in
  let f1, points = step_n grid len len points in
  let f2, _ = step_n grid len len points in
  let n = (26501365 - 65) / len in
  let part2 = solve_quadratic [| f0; f1; f2 |] n in

  Answer.part1 3847 part1 string_of_int;
  Answer.part2 637537341306357 part2 string_of_int

let () = Answer.timer solution
