let get_nth s i = List.nth (String.split_on_char ' ' s) i

(* 5 blue*)
let parse_ball s = (get_nth s 2, int_of_string (get_nth s 1))

(* <ball_1>, <ball_2>, <ball_3>*)
let parse_ball_set s = List.map parse_ball (String.split_on_char ',' s)

type ball_game = { id : int; ball_sets : (string * int) list list }

let get_id game = game.id

(*Game <id>: <ball_set_1>; <ball_set_2>; <ball_set_3>*)
let parse_game s =
  match String.split_on_char ':' s with
  | [ game_id; ball_sets ] ->
      {
        id = int_of_string (get_nth game_id 1);
        ball_sets = List.map parse_ball_set (String.split_on_char ';' ball_sets);
      }
  | _ -> raise (Invalid_argument s)

let valid_ball balls n color =
  match List.assoc_opt color balls with
  | Some max_n -> n <= max_n
  | None -> false

let rec valid_ball_set balls ball_set =
  match ball_set with
  | (color, n) :: xs ->
      if valid_ball balls n color then valid_ball_set balls xs else false
  | _ -> true

let rec valid_ball_sets balls ball_sets =
  match ball_sets with
  | ball_set :: xs ->
      if valid_ball_set balls ball_set then valid_ball_sets balls xs else false
  | _ -> true

let valid_game balls game = valid_ball_sets balls game.ball_sets

let get_ball color ball_set =
  match List.assoc_opt color ball_set with Some value -> value | None -> 0

let rec min_set result ball_sets =
  match ball_sets with
  | ball_set :: xs ->
      let updated_result =
        [
          ("red", max (get_ball "red" result) (get_ball "red" ball_set));
          ("blue", max (get_ball "blue" result) (get_ball "blue" ball_set));
          ("green", max (get_ball "green" result) (get_ball "green" ball_set));
        ]
      in
      min_set updated_result xs
  | _ -> result

let min_set_power game =
  let result = min_set [] game.ball_sets in
  get_ball "red" result * get_ball "blue" result * get_ball "green" result

let () =
  let values = Aoc.Reader.read_lines () in
  let games = List.map parse_game values in
  let balls = [ ("red", 12); ("green", 13); ("blue", 14) ] in
  let valid_games = List.filter (valid_game balls) games in
  let part1 = List.fold_left ( + ) 0 (List.map get_id valid_games) in
  let part2 = List.fold_left ( + ) 0 (List.map min_set_power games) in
  Aoc.Answer.part1 2348 part1 string_of_int;
  Aoc.Answer.part2 76008 part2 string_of_int
