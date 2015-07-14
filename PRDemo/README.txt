Extract as follows:

node_modules.tgz --> /usr/lib/node_modules
python2.7.tgz --> /usr/lib/python2.7
edison_config_tools.tgz /usr/lib/edison_config_tools
system.tgz --> /etc/systemd/system
home.tgz --> /home/root

Installation:

	-Extract all archives to directories
	-chmod +x  /usr/lib/edison_config_tools/edison-config-server.js
	-chmod +x  /usr/lib/edison_config_tools/db-init.js
	-chmod +x /home/root/brizastartup.sh
	-chmod +x /home/root/sense.sh
	-systemctl enable briza.service

Service should now start on reboot
