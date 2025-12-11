defmodule AdventOfCode.MixProject do
  use Mix.Project

  def project do
    [
      app: :advent_of_code,
      version: "0.1.0",
      elixir: "~> 1.14",
      elixirc_paths: elixirc_paths(),
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  defp elixirc_paths do
    ["lib/elixir"] ++ Path.wildcard("2???/??")
  end

  def application do
    [extra_applications: [:logger]]
  end

  defp deps do
    []
  end
end
