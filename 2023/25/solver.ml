open Aoc
open Core

module Node = struct
  type t = { name : string; count : int }
  [@@deriving compare, equal, hash, sexp]
end

type graph = (Node.t, Node.t list) Hashtbl.t

let add (n : Node.t) (s : Node.t list option) : Node.t list =
  match s with None -> [ n ] | Some s -> n :: s

let add_nodes (g : graph) (n1 : string) (n2 : string) : unit =
  let n1 : Node.t = { name = n1; count = 1 } in
  let n2 : Node.t = { name = n2; count = 1 } in
  Hashtbl.update g n1 ~f:(add n2);
  Hashtbl.update g n2 ~f:(add n1)

let add_edges (g : graph) (s : string) : unit =
  match Str.split (Str.regexp ": ") s with
  | [ node; edges ] ->
      let edges = String.split ~on:' ' edges in
      List.iter ~f:(add_nodes g node) edges
  | _ -> raise (Invalid_argument s)

let get_and_remove (g : graph) (node : Node.t) (remove : Node.t) : Node.t list =
  let edges = Hashtbl.find_exn g node in
  let edges = List.filter ~f:(fun edge -> not (Node.equal edge remove)) edges in
  Hashtbl.remove g node;
  edges

let replace (g : graph) (old_value : Node.t) (new_value : Node.t)
    (neighbor : Node.t) =
  let edges =
    List.map
      ~f:(fun edge -> if Node.equal edge old_value then new_value else edge)
      (Hashtbl.find_exn g neighbor)
  in
  Hashtbl.set g ~key:neighbor ~data:edges

let combine (g : graph) (n1 : Node.t) (n2 : Node.t) =
  let edges1 = get_and_remove g n1 n2 in
  let edges2 = get_and_remove g n2 n1 in
  let combined = { n1 with count = n1.count + n2.count } in
  Hashtbl.set g ~key:combined ~data:(edges1 @ edges2);
  List.iter ~f:(replace g n1 combined) edges1;
  List.iter ~f:(replace g n2 combined) edges2

let random_element (values : Node.t list) : Node.t =
  List.nth_exn values (Random.int (List.length values))

let rec karger (g : graph) : graph =
  match Hashtbl.length g > 2 with
  | false -> g
  | true ->
      let n1 = random_element (Hashtbl.keys g) in
      let n2 = random_element (Hashtbl.find_exn g n1) in
      combine g n1 n2;
      karger g

let cut_size (g : graph) : int = List.length (List.hd_exn (Hashtbl.data g))

let rec until_cut_size (g : graph) (size : int) =
  let reduced = karger (Hashtbl.copy g) in
  if Int.equal (cut_size reduced) size then reduced else until_cut_size g size

let node_sizes (g : graph) : int list =
  List.map ~f:(fun (node : Node.t) : int -> node.count) (Hashtbl.keys g)

let solution () =
  let graph : graph = Hashtbl.create (module Node) in
  let values = Reader.read_lines () in
  List.iter ~f:(add_edges graph) values;
  let graph = until_cut_size graph 3 in
  let part1 = Util.multiply (node_sizes graph) in
  Answer.part1 567606 part1 string_of_int

let () = Answer.timer solution
