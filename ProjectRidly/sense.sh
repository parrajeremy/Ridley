(cd /home/root && python /home/root/Ridley/ProjectRidly/sensesock.py) &
#sleep 2
(cd /home/root && python /home/root/Ridley/ProjectRidly/briza_eeprom_v3.py 0x53 0x55 0x56 0x57) &
sleep 2
(cd /home/root && python /home/root/Ridley/ProjectRidly/briza_v3.py 0x53 0x55 0x56 0x57) &