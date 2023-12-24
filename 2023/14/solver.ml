open Core

let get_max grid f =
  let values = List.map ~f (Hashtbl.keys grid) in
  Aoc.Util.max values + 1

let find_rocks grid direction =
  let points =
    Hashtbl.to_alist grid
    |> List.filter ~f:(fun (_, ch) -> Char.equal ch 'O')
    |> List.map ~f:(fun (p, _) -> p)
  in
  match direction with
  | Aoc.Direction.UP ->
      List.sort ~compare:(fun a b -> Int.compare a.Aoc.Point.y b.y) points
  | DOWN -> List.sort ~compare:(fun a b -> Int.compare b.y a.y) points
  | LEFT -> List.sort ~compare:(fun a b -> Int.compare a.x b.x) points
  | RIGHT -> List.sort ~compare:(fun a b -> Int.compare b.x a.x) points

let rec move_rock grid direction rock =
  let next =
    match direction with
    | Aoc.Direction.UP -> { rock with Aoc.Point.y = rock.Aoc.Point.y - 1 }
    | DOWN -> { rock with y = rock.y + 1 }
    | LEFT -> { rock with x = rock.x - 1 }
    | RIGHT -> { rock with x = rock.x + 1 }
  in
  let can_move =
    match Hashtbl.find grid next with
    | None -> false
    | Some value -> Char.equal '.' value
  in
  match can_move with
  | false -> ()
  | true ->
      Hashtbl.remove grid rock;
      Hashtbl.add_exn grid ~key:rock ~data:'.';
      Hashtbl.remove grid next;
      Hashtbl.add_exn grid ~key:next ~data:'O';
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

let get_load grid max_y =
  let rocks = find_rocks grid UP in
  Aoc.Util.sum (List.map ~f:(fun p -> max_y - p.Aoc.Point.y) rocks)

let run_cycle grid =
  find_and_move grid UP;
  find_and_move grid LEFT;
  find_and_move grid DOWN;
  find_and_move grid RIGHT

let grid_row grid xs y =
  let chars =
    List.map ~f:(fun x -> Hashtbl.find_exn grid { Aoc.Point.x; y }) xs
  in
  String.of_char_list chars

let grid_string grid max_x max_y =
  let xs = List.init max_x ~f:(fun x -> x) in
  let ys = List.init max_y ~f:(fun y -> y) in
  let rows = List.map ~f:(grid_row grid xs) ys in
  String.concat ~sep:"\n" rows

let rec until_repeat grid max_x max_y seen =
  run_cycle grid;
  let as_string = grid_string grid max_x max_y in
  match List.Assoc.find ~equal:String.equal seen as_string with
  | None ->
      let next = get_load grid max_y in
      until_repeat grid max_x max_y ((as_string, next) :: seen)
  | Some _ ->
      let result = List.rev seen in
      let preamble, _ =
        Option.value_exn
          (List.findi ~f:(fun _ (x, _) -> String.equal x as_string) result)
      in
      let pattern = List.filteri ~f:(fun i _ -> i >= preamble) result in
      let pattern = List.map ~f:(fun (_, x) -> x) pattern in
      (preamble, pattern)

let () =
  let grid = Aoc.Reader.read_grid_table () in
  let max_x = get_max grid (fun p -> p.Aoc.Point.x) in
  let max_y = get_max grid (fun p -> p.Aoc.Point.y) in

  find_and_move grid UP;
  let part1 = get_load grid max_y in

  (* Complete the first cycle *)
  find_and_move grid LEFT;
  find_and_move grid DOWN;
  find_and_move grid RIGHT;

  let starting_seen = [ (grid_string grid max_x max_y, get_load grid max_y) ] in
  let preamble, pattern = until_repeat grid max_x max_y starting_seen in
  let pattern_index = (1000000000 - 1 - preamble) mod List.length pattern in
  let part2 = List.nth_exn pattern pattern_index in
  Aoc.Answer.part1 109654 part1 string_of_int;
  Aoc.Answer.part2 94876 part2 string_of_int
