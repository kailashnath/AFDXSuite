#!/bin/sh

OUTPUT_DIR=$1
OUTPUT_FILENAME=$2
CAPTURE_FILTER=$3

chmod 777 "$OUTPUT_DIR"
dumpcap -f "$CAPTURE_FILTER" -M -w "$OUTPUT_DIR/$OUTPUT_FILENAME" 2> /dev/null &

echo $! > "/tmp/pyid_$OUTPUT_FILENAME"
