#!/bin/bash
# This script could be used along with netcat
# such as: nc -l -p 7001 | sh echo_server.sh
while IFS= read -r line
do
  echo "$line"
done
