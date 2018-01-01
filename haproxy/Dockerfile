FROM haproxy:alpine
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

RUN apk --no-cache add socat

EXPOSE 587

ENTRYPOINT haproxy -f /usr/local/etc/haproxy/haproxy.cfg -db
