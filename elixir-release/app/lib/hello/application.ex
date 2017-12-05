defmodule Hello.Application do

  def start(_type, _args) do
    children = [
      {Hello, []},
    ]

    opts = [strategy: :one_for_one, name: Hello.Supervisor]
    Supervisor.start_link(children, opts)
  end

end
