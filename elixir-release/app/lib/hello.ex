defmodule Hello do
  @moduledoc """
  Hello World Module
  """

  use GenServer, restart: :temporary

  def start_link(_) do
    GenServer.start_link(__MODULE__, :ok)
  end

  def handle_info(:timeout, 1000) do
    IO.puts("Hello World")
    {:noreply, 1000, 1000}
  end
end
