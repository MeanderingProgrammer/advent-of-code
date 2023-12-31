open Core

type graph = (string, string list) Hashtbl.t

let add (n : string) (s : string list option) : string list =
  match s with None -> [ n ] | Some s -> n :: s

let add_nodes (g : graph) (n1 : string) (n2 : string) : unit =
  Hashtbl.update g n1 ~f:(add n2);
  Hashtbl.update g n2 ~f:(add n1)

let add_edges (g : graph) (s : string) : unit =
  match Str.split (Str.regexp ": ") s with
  | [ node; edges ] ->
      let edges = String.split ~on:' ' edges in
      List.iter ~f:(add_nodes g node) edges
  | _ -> raise (Invalid_argument s)

let get_and_remove (g : graph) (node : string) (remove : string) : string list =
  let edges = Hashtbl.find_exn g node in
  let edges =
    List.filter ~f:(fun edge -> not (String.equal edge remove)) edges
  in
  Hashtbl.remove g node;
  edges

let replace (g : graph) (old_value : string) (new_value : string)
    (neighbor : string) =
  let edges =
    List.map
      ~f:(fun edge -> if String.equal edge old_value then new_value else edge)
      (Hashtbl.find_exn g neighbor)
  in
  Hashtbl.set g ~key:neighbor ~data:edges

let combine (g : graph) (n1 : string) (n2 : string) =
  let edges1 = get_and_remove g n1 n2 in
  let edges2 = get_and_remove g n2 n1 in
  let combined = n1 ^ "+" ^ n2 in
  Hashtbl.set g ~key:combined ~data:(edges1 @ edges2);
  List.iter ~f:(replace g n1 combined) edges1;
  List.iter ~f:(replace g n2 combined) edges2

let random_element (values : string list) : string =
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
  let node_size (node : string) : int =
    List.length (String.split ~on:'+' node)
  in
  List.map ~f:node_size (Hashtbl.keys g)

let () =
  let graph : graph = Hashtbl.create (module String) in
  let values = Aoc.Reader.read_lines () in
  List.iter ~f:(add_edges graph) values;
  let graph = until_cut_size graph 3 in
  let part1 = Aoc.Util.multiply (node_sizes graph) in
  Aoc.Answer.part1 567606 part1 string_of_int
