FROM alpine

WORKDIR /app

RUN apk add --no-cache squid && \
    mkdir -p /var/cache/squid

RUN rm -rf ~/.cache

EXPOSE 3128

ENTRYPOINT [ "/start-squid" ]

COPY start-squid /start-squid
COPY squid.conf /etc/squid/squid.conf
COPY outbound_whitelist.txt /etc/squid/

# force patches through --build-arg
ARG BUILD_VERSION
RUN echo $BUILD_VERSION && apk upgrade --no-cache

