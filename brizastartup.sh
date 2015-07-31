#!/bin/bash

sh /home/root/Briza/sense.sh 
sleep 5
(cd /usr/lib/edison_config_tools && node /usr/lib/edison_config_tools/edison-config-server.js) 


