# Minecraft Server VPS Scripts  

#### Running  
Assuming a brand new server  

First things first:
```sh
# Clone Repo
git clone https://github.com/EniMiniGames/MC-Server-VPS-Scripts.git .  

# Move scripts into current working dir
mv -t . MC-Server-VPS-Scripts/*.sh MC-Server-VPS-Scripts/*.py

# Mark as executable
chmod +x *.sh *.py  

# Install required packages
./pre_installations.sh
```  

#### Server Setup  
```sh  

# Run setup
# Might take a bit to download/install packages, and run BuildTools
./server_vps_setup.sh   

cd server  

./start_server_screen.sh  
# And the server should be up!  
```  

To view the server console, do 
`screen -r`  

To exit that hit `Ctrl + A + D` or `Ctrl + A THEN Ctrl + D`  


#### BungeeCord  
Do the instructions above first. Run and stop the server once.

```sh  
cd ~
# Setup Bungee stuff
# These first commands can be skipped if running Bungee on a different server
./bungee_vps_setup.sh
mv -t bungee start_bungee_screen.sh bungee_startup_loop.sh

# Edit server properties for Bungee usage
# *Add localhost arg if running Bungee on same server*
# This can be skipped if there are no servers running on the host

./set_offline_mode.py server localhost
./set_server_bungee_mode.py server

cd bungee
./start_bungee_screen.sh	
# Ctrl + C to stop

# Run bungee once, then run
../enable_bungee_ip_forward.py .
```  

#### TODO  

- [ ] Firewalls  
- [ ] Comment scripts  
- [x] spigot.yml, bungeecord: true script
- [x] Bungee config.yml ip_forward: true script
- [ ] Use DO API to do all this. Bungee on 512MB server, Lobby on 1GB server, rest on whatever.
- [ ] Use DO-API in Bungee plugin to spin up new server for each gamemode.
- [ ] Add to /etc/rc.local 