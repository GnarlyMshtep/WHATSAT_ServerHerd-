#!/bin/bash

#a simple script for interminent testing 
python3 server.py Johnson &
python3 server.py Bernard &
python3 server.py Juzang &

sleep 2s
time_1=`date +%s` 
python3 client.py 10394 "IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 ${time_1}" 
(( time_2 = time_1 + 2 ))
python3 client.py 10394 "IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 ${time_2}" 
(( time_3 = time_2 + 2 ))
python3 client.py 10394 "IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 ${time_3}"
python3 client.py 10394 "IAMAT spicli +232323-89123.122 ${time_3}"


sleep 4s #let things occuer
echo '----------------------------'
pkill -f server.py #?try to kill the servers in case of failure, ussuly this yields errs, but that's ok 
echo '----------------------------'

# netstat -tulpn | grep 1039 to find my ports in use
# then kill pid