type hand_type =
  | FIVE_KIND
  | FOUR_KIND
  | HOUSE
  | THREE_KIND
  | TWO_PAIR
  | PAIR
  | CARD

let to_value t =
  match t with
  | FIVE_KIND -> 7
  | FOUR_KIND -> 6
  | HOUSE -> 5
  | THREE_KIND -> 4
  | TWO_PAIR -> 3
  | PAIR -> 2
  | CARD -> 1

type hand = { cards : char list; bid : int }

(* 32T3K 765 *)
let parse_hand s =
  match String.split_on_char ' ' s with
  | cards :: bid :: _ ->
      { cards = List.of_seq (String.to_seq cards); bid = int_of_string bid }
  | _ -> raise (Invalid_argument s)

let count cards card =
  List.length (List.filter (fun ch -> Char.compare ch card == 0) cards)

let card_value wild_joker card =
  match card with
  | 'A' -> 14
  | 'K' -> 13
  | 'Q' -> 12
  | 'J' -> if wild_joker then 1 else 11
  | 'T' -> 10
  | _ -> int_of_char card - int_of_char '0'

let get_count value values =
  List.length (List.find_all (fun v -> v == value) values)

let get_hand_type wild_joker cards =
  let values =
    [
      count cards 'A';
      count cards 'K';
      count cards 'Q';
      count cards 'T';
      count cards '9';
      count cards '8';
      count cards '7';
      count cards '6';
      count cards '5';
      count cards '4';
      count cards '3';
      count cards '2';
    ]
  in
  let values = if wild_joker then values else count cards 'J' :: values in
  let max = List.fold_left Int.max (List.hd values) (List.tl values) in
  let jokers = if wild_joker then count cards 'J' else 0 in
  let num_2 = get_count 2 values in
  if max + jokers == 5 then FIVE_KIND
  else if max + jokers == 4 then FOUR_KIND
  else if (max == 3 && num_2 == 1) || (num_2 == 2 && jokers == 1) then HOUSE
  else if max + jokers == 3 then THREE_KIND
  else if max == 2 && num_2 == 2 then TWO_PAIR
  else if max + jokers == 2 then PAIR
  else CARD

let rec compare_cards wild_joker cards =
  match cards with
  | (a, b) :: xs ->
      if a == b then compare_cards wild_joker xs
      else Int.compare (card_value wild_joker a) (card_value wild_joker b)
  | [] -> 0

let compare_hands wild_joker a b =
  let a_type = get_hand_type wild_joker a.cards in
  let b_type = get_hand_type wild_joker b.cards in
  let type_comparison = Int.compare (to_value a_type) (to_value b_type) in
  if type_comparison != 0 then type_comparison
  else compare_cards wild_joker (List.combine a.cards b.cards)

let winnings i h = (i + 1) * h.bid

let total_winnings hands wild_joker =
  let comparison = compare_hands wild_joker in
  let ordered = List.sort comparison hands in
  List.fold_left ( + ) 0 (List.mapi winnings ordered)

let () =
  let values = Aoc.Reader.read_lines () in
  let hands = List.map parse_hand values in
  let part1 = total_winnings hands false in
  let part2 = total_winnings hands true in
  Aoc.Answer.part1 248105065 part1 string_of_int;
  Aoc.Answer.part2 249515436 part2 string_of_int
