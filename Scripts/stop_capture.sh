#!/bin/sh

chmod -R 777 ./captures/
ps -e -o pid,command | grep $1 | gawk -F " " '{print "kill -9 ", $1;}' > /tmp/cap_pids

bash /tmp/cap_pids 2> /tmp/null

rm /tmp/cap_pids

