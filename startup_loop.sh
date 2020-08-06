#!/bin/sh

while true
do
	# rm -rf world
	# cp -r spleef_world world
	
	# Runs to infinity 
	java -Xms1G -Xmx2G -jar spigot-1.15.2.jar nogui

	echo "If you want to completely stop the server process now, press Ctrl+C b$"
	echo "Rebooting in:"
	
	for i in 5 4 3 2 1
		do
		echo "$i..."
		sleep 1
	done
	
	echo "Rebooting now!"
done

# su -c "screen -S screenname -d -m bash /path/to/your/start/script.sh" yourusername
# in your /etc/rc.local and the server will start automatically when you reboot your server.
