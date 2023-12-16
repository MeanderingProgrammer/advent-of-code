open Aoc.Point

let find_rocks grid direction =
  let rocks = List.filter (fun (_, ch) -> ch == 'O') !grid in
  let points = List.map (fun (p, _) -> p) rocks in
  match direction with
  | UP -> List.sort (fun a b -> Int.compare a.y b.y) points
  | DOWN -> List.sort (fun a b -> Int.compare b.y a.y) points
  | LEFT -> List.sort (fun a b -> Int.compare a.x b.x) points
  | RIGHT -> List.sort (fun a b -> Int.compare b.x a.x) points

let rec move_rock grid direction rock =
  let next =
    match direction with
    | UP -> { rock with y = rock.y - 1 }
    | DOWN -> { rock with y = rock.y + 1 }
    | LEFT -> { rock with x = rock.x - 1 }
    | RIGHT -> { rock with x = rock.x + 1 }
  in
  let can_move =
    match List.assoc_opt next !grid with
    | None -> false
    | Some value -> Char.equal '.' value
  in
  match can_move with
  | false -> ()
  | true ->
      grid := List.remove_assoc rock !grid;
      grid := (rock, '.') :: !grid;
      grid := List.remove_assoc next !grid;
      grid := (next, 'O') :: !grid;
      move_rock grid direction next

let rec move_rocks grid direction rocks =
  match rocks with
  | [] -> ()
  | x :: xs ->
      move_rock grid direction x;
      move_rocks grid direction xs

let find_and_move grid direction =
  let rocks = find_rocks grid direction in
  move_rocks grid direction rocks

let get_load grid =
  let ys = List.map (fun (p, _) -> p.y) !grid in
  let max_y = List.fold_left Int.max (List.hd ys) (List.tl ys) + 1 in
  let rocks = find_rocks grid UP in
  let values = List.map (fun p -> max_y - p.y) rocks in
  List.fold_left ( + ) 0 values

let rec run_cycle grid i =
  match i with
  | 0 -> ()
  | _ ->
      find_and_move grid UP;
      find_and_move grid LEFT;
      find_and_move grid DOWN;
      find_and_move grid RIGHT;
      Printf.printf "LOAD = %d\n" (get_load grid);
      run_cycle grid (i - 1)

let () =
  let grid = ref (Aoc.Reader.read_grid ()) in
  find_and_move grid UP;
  let part1 = get_load grid in
  find_and_move grid LEFT;
  find_and_move grid DOWN;
  find_and_move grid RIGHT;
  run_cycle grid 100;
  (* Aoc.Answer.part1 136 part1 string_of_int *)
  Aoc.Answer.part1 109654 part1 string_of_int
