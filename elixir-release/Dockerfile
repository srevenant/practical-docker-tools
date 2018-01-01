FROM elixir:alpine
WORKDIR /app/

COPY app /app/

# build the application into a binary release
RUN mix local.hex --force && \
    mix local.rebar --force && \
    mix do deps.get, deps.compile && \
    mix release.init && mix release

# switch to a new base image
#FROM elixir:alpine
#
#WORKDIR /app
#RUN apk --no-cache add bash
#
## copy only our binary release from the first image into the new image
#COPY --from=0 /app/_build/dev/rel/hello /app/
#
#CMD /app/bin/hello console
