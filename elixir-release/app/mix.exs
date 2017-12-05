defmodule Hello.Mixfile do
  use Mix.Project

  def project do
    [
      app: :hello,
      version: "1.0.0",
      elixir: "~> 1.5",
      start_permanent: Mix.env == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      mod: {Hello.Application, []},
      extra_applications: [:logger]
    ]
  end

  defp deps do
    [
      {:distillery, "~> 1.5"}
    ]
  end
end

