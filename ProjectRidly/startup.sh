#!/bin/sh
echo "src/gz all http://repo.opkg.net/edison/repo/all" > /etc/opkg/base-feeds.conf
echo "src/gz edison http://repo.opkg.net/edison/repo/edison" > /etc/opkg/base-feeds.conf
echo "src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32" > /etc/opkg/base-feeds.conf
echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf
opkg update
git clone https://github.com/isclayton/Ridley.git
#opkg upgrade
opkg install git
echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic-dev" > /etc/opkg/mraa-upm.conf 
opkg update 
opkg install libmraa0 
curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
sleep 1
python get-pip.py
#pip install pyserial

opkg install "python-numpy"
opkg install sqlite3
opkg install "python-sqlite3"
npm install sqlite3 -g
npm install express -g
npm install require -g
npm install lodash.repeat -g
npm install logger -g
npm install python-shell -g
cp -R /home/root/Ridley/ProjectRidly/web/* /usr/lib/edison_config_tools/
cp -R /home/root/Ridley/ProjectRidly/system/* /etc/systemd/system/
chmod +x  /usr/lib/edison_config_tools/edison-config-server.js
chmod +x  /usr/lib/edison_config_tools/public/dbint.js
chmod +x /home/root/Ridley/ProjectRidly/brizastartup.sh
chmod +x /home/root/Ridley/ProjectRidly/sense.sh
#python /home/root/Ridley/ProjectRidly/briza_eeprom.py
systemctl daemon-reload
systemctl disable edison_config.service
systemctl disable pwr-button-handler.service
systemctl enable pwr-button-handler.service
systemctl enable briza.service
systemctl 
system
#reboot

