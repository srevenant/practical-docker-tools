#!/bin/sh
/sbin/syslogd -O /proc/1/fd/1
exec node hello.js
