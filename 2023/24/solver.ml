open Aoc
open Core

type point = { x : float; y : float; z : float }
type stone = { position : point; velocity : point }

let parse_float (s : string) : float =
  float_of_int (int_of_string (String.strip s))

(* 19, 13, 30 *)
let parse_point (s : string) : point =
  match Str.split (Str.regexp ", ") s with
  | [ x; y; z ] -> { x = parse_float x; y = parse_float y; z = parse_float z }
  | _ -> raise (Invalid_argument s)

(* <position> @ <velocity> *)
let parse_stone (s : string) : stone =
  match Str.split (Str.regexp " @ ") s with
  | [ position; velocity ] ->
      { position = parse_point position; velocity = parse_point velocity }
  | _ -> raise (Invalid_argument s)

let rec each_pair (s : stone) (stones : stone list) : (stone * stone) list =
  match stones with [] -> [] | x :: xs -> (s, x) :: each_pair s xs

let rec all_pairs (stones : stone list) : (stone * stone) list =
  match stones with [] -> [] | x :: xs -> each_pair x xs @ all_pairs xs

let pull_xy (p : point) : float * float = (p.x, p.y)
let pull_xz (p : point) : float * float = (p.x, p.z)

let solve_t (s1 : stone) (s2 : stone) : float option =
  (* y1 - y2 - vy2((x1 - x2)/vx2) = (vy2(vx1/vx2) - vy1)t1 *)
  let (x1, y1), (vx1, vy1) = (pull_xy s1.position, pull_xy s1.velocity) in
  let (x2, y2), (vx2, vy2) = (pull_xy s2.position, pull_xy s2.velocity) in
  let lhs = y1 -. y2 -. (vy2 *. ((x1 -. x2) /. vx2)) in
  let rhs = (vy2 *. (vx1 /. vx2)) -. vy1 in
  match rhs with
  | 0. -> None
  | _ -> (
      let t = lhs /. rhs in
      match Float.compare t 0. < 0 with true -> None | false -> Some t)

let intersects (between : float -> bool) ((s1, s2) : stone * stone) : bool =
  match (solve_t s1 s2, solve_t s2 s1) with
  | Some t, Some _ ->
      let (x, y), (vx, vy) = (pull_xy s1.position, pull_xy s1.velocity) in
      between (x +. (vx *. t)) && between (y +. (vy *. t))
  | _ -> false

(* https://www.reddit.com/r/adventofcode/comments/18q40he/2023_day_24_part_2_a_straightforward_nonsolver/ *)
let create_row (pull : point -> float * float) (s : stone) : float list =
  (* (dy'-dy)X + (dx-dx')Y + (y-y')DX + (x'-x)DY = x'dy' - y'dx' - xdy + ydx *)
  let (x, y), (dx, dy) = (pull s.position, pull s.velocity) in
  [ -1. *. dy; dx; y; -1. *. x; (y *. dx) -. (x *. dy) ]

let create_matrix (stones : stone list) (pull : point -> float * float) :
    float list array =
  let rows = List.map ~f:(create_row pull) stones in
  let last_row = List.last_exn rows in
  let subtract (row : float list) : float list =
    List.map ~f:(fun (a, b) -> a -. b) (List.zip_exn row last_row)
  in
  (* Row equation has 4 unknowns hence we take 4 rows for equations *)
  Array.map ~f:subtract (List.to_array (List.take rows 4))

let gaussian_elimination (matrix : float list array) : int list =
  let size = Array.length matrix in
  for i = 0 to size - 1 do
    let t = List.nth_exn matrix.(i) i in
    matrix.(i) <- List.map ~f:(fun x -> x /. t) matrix.(i);
    for j = i + 1 to size - 1 do
      let t = List.nth_exn matrix.(j) i in
      matrix.(j) <-
        List.mapi
          ~f:(fun k x -> x -. (t *. List.nth_exn matrix.(i) k))
          matrix.(j)
    done
  done;
  for i = size - 1 downto 0 do
    for j = 0 to i - 1 do
      let t = List.nth_exn matrix.(j) i in
      matrix.(j) <-
        List.mapi
          ~f:(fun k x -> x -. (t *. List.nth_exn matrix.(i) k))
          matrix.(j)
    done
  done;
  let result = Array.map ~f:(fun row -> List.last_exn row) matrix in
  Array.to_list (Array.map ~f:int_of_float result)

let () =
  let values = Reader.read_lines () in
  let stones = List.map ~f:parse_stone values in
  let between = Float.between ~low:200000000000000. ~high:400000000000000. in
  let part1 = List.count ~f:(intersects between) (all_pairs stones) in
  let l1 = gaussian_elimination (create_matrix stones pull_xy) in
  let x, y = (List.nth_exn l1 0, List.nth_exn l1 1) in
  let l2 = gaussian_elimination (create_matrix stones pull_xz) in
  let _, z = (List.nth_exn l2 0, List.nth_exn l2 1) in
  let part2 = x + y + z in
  Answer.part1 14672 part1 string_of_int;
  Answer.part2 646810057104753 part2 string_of_int
