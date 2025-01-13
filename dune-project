(lang dune 3.15)

(name advent_of_code)

(source
  (github MeanderingProgrammer/advent-of-code))

(generate_opam_files true)

(authors "MeanderingProgrammer <meanderingprogrammer@gmail.com>")

(maintainers "MeanderingProgrammer <meanderingprogrammer@gmail.com>")

(license MIT)

(package
 (name advent_of_code)
 (synopsis "Advent of Code - All Years - Blazingly Fast")
 (description "Advent of Code - All Years - Blazingly Fast")
 (depends ocaml dune core_kernel ppx_jane ppx_sexp_conv ppx_expect))
