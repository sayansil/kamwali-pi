#!/bin/bash

wait_for(){
    seq $1 -1 1 | while read j; do echo -en "\r$j seconds remaining     ";sleep 1;done;echo
}

clear
echo "Preparing to launch scripts"
wait_for 20

n=2
i=0

success_verbose(){
    i=$(($i+1))
    echo "$i/$n - Running $1"
}


cd /home/pi/Desktop/iot/diagnostics
lxterminal --command="python3 /home/pi/Desktop/iot/diagnostics/main.py"
success_verbose "diagnostics"

cd /home/pi/Desktop/iot/mqtt
lxterminal --command="python3 /home/pi/Desktop/iot/mqtt/subscriber.py"
success_verbose "mqtt service"

echo "All services running."
