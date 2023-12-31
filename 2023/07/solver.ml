open Aoc
open Core

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
  match String.split ~on:' ' s with
  | [ cards; bid ] -> { cards = String.to_list cards; bid = int_of_string bid }
  | _ -> raise (Invalid_argument s)

let count cards card = List.count ~f:(Char.equal card) cards

let card_value wild_joker card =
  match card with
  | 'A' -> 14
  | 'K' -> 13
  | 'Q' -> 12
  | 'J' -> if wild_joker then 1 else 11
  | 'T' -> 10
  | _ -> Char.get_digit_exn card

let get_count value values = List.count ~f:(Int.equal value) values

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
  let max = Util.max values in
  let jokers = if wild_joker then count cards 'J' else 0 in
  let num_2 = get_count 2 values in
  if Int.equal (max + jokers) 5 then FIVE_KIND
  else if Int.equal (max + jokers) 4 then FOUR_KIND
  else if
    (Int.equal max 3 && Int.equal num_2 1)
    || (Int.equal num_2 2 && Int.equal jokers 1)
  then HOUSE
  else if Int.equal (max + jokers) 3 then THREE_KIND
  else if Int.equal max 2 && Int.equal num_2 2 then TWO_PAIR
  else if Int.equal (max + jokers) 2 then PAIR
  else CARD

let rec compare_cards wild_joker cards =
  match cards with
  | (a, b) :: xs ->
      if Char.equal a b then compare_cards wild_joker xs
      else Int.compare (card_value wild_joker a) (card_value wild_joker b)
  | [] -> 0

let compare_hands wild_joker a b =
  let a_type = get_hand_type wild_joker a.cards in
  let b_type = get_hand_type wild_joker b.cards in
  let type_comparison = Int.compare (to_value a_type) (to_value b_type) in
  if not (Int.equal type_comparison 0) then type_comparison
  else compare_cards wild_joker (List.zip_exn a.cards b.cards)

let winnings i h = (i + 1) * h.bid

let total_winnings hands wild_joker =
  let compare = compare_hands wild_joker in
  let ordered = List.sort ~compare hands in
  Util.sum (List.mapi ~f:winnings ordered)

let () =
  let values = Reader.read_lines () in
  let hands = List.map ~f:parse_hand values in
  let part1 = total_winnings hands false in
  let part2 = total_winnings hands true in
  Answer.part1 248105065 part1 string_of_int;
  Answer.part2 249515436 part2 string_of_int
