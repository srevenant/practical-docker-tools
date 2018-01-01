#!/bin/sh
# identify our parent host IP
hostip=$(ip route show | awk '/default/ {print $3}')
# locally mount host /var/log/email:/var/log
cat > /etc/rsyslog.conf <<END
\$ModLoad imuxsock
\$AddUnixListenSocket /dev/log
\$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
*.* @@$hostip:514
END
mkdir /var/lib/rsyslog
rsyslogd
exec node hello.js
