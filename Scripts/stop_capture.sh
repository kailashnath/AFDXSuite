#!/bin/sh

chmod -R 777 ./captures/
#ps -e -o pid,command | grep $1 | gawk -F " " '{print "kill -9 ", $1;}' > /tmp/cap_pids

kill -9 `ps -e -o pid,command | grep dumpcap | cut -d" " -f2`

