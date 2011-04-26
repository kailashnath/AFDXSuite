#!/bin/sh

PROGRAM=$1
OUTPUT_DIR=$2

chmod -R 777 "$OUTPUT_DIR"
#ps -e -o pid,command | grep $1 | gawk -F " " '{print "kill -9 ", $1;}' > /tmp/cap_pids

#kill -9 `ps -e -o pid,command | grep dumpcap | cut -d" " -f1`
pkill $PROGRAM

