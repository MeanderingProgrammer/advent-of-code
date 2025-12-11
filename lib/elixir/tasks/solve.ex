defmodule Mix.Tasks.Solve do
  use Mix.Task

  @impl Mix.Task
  def run([year, day | args]) do
    # additional args are passed through
    System.argv(args)

    module = Module.concat(["Solver", "Y#{year}", "D#{day}"])

    if Code.ensure_loaded?(module) do
      start_time = System.monotonic_time(:nanosecond)
      module.main()
      end_time = System.monotonic_time(:nanosecond)
      IO.puts("Runtime (ns): #{end_time - start_time}")
    else
      Mix.shell().error("Module #{inspect(module)} not found")
    end
  end

  def run(_) do
    Mix.shell().error("Usage: mix solve <year> <day> [args...]")
  end
end
