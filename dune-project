(lang dune 3.15)

(name advent_of_code)

(source
  (github MeanderingProgrammer/advent-of-code))

(generate_opam_files true)

(authors "MeanderingProgrammer <meanderingprogrammer@gmail.com>")

(maintainers "MeanderingProgrammer <meanderingprogrammer@gmail.com>")

(package
 (name advent_of_code)
 (synopsis "Public Repo for Advent of Code Solutions")
 (description "Public Repo for Advent of Code Solutions")
 (depends ocaml dune core_kernel ppx_jane ppx_sexp_conv ppx_expect))
