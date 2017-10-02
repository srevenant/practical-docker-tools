FROM elixir:alpine
WORKDIR /app/
RUN apk --no-cache add nodejs yarn inotify-tools && \
    mix local.hex --force && \
    mix local.rebar --force && \
    mix archive.install --force https://github.com/phoenixframework/archives/raw/master/phx_new.ez && \
    mix phx.new hello
WORKDIR /app/hello
RUN sed -i -e 's/hostname: "localhost"/hostname: "postgres"/' config/dev.exs && \
    mix do deps.get, deps.compile && \
    cd assets && \
        yarn install

CMD mix do ecto.create, phx.server
