#!/bin/bash

sh /home/root/Ridley/ProjectRidly/sense.sh 
sleep 5
(cd /usr/lib/edison_config_tools && node /usr/lib/edison_config_tools/edison-config-server.js) 


