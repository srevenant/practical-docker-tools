# Squid Proxy

Outbound proxy service for backend services in a network controlled world (not all outbound access is allowed).

Allows all 10.0.0.0/8 and 172.16.0.0/16 networks to use the service.

Allows outbound access based on the file `outbound_whitelist.txt` as a list of allowed regex hosts.

