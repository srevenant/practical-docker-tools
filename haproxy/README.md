# using HA proxy for SMTP

Uses haproxy for SMTP out to external email service.  useful on a network restricted zone

Map to host's syslog because haproxy only does syslog/datagrams for logging
