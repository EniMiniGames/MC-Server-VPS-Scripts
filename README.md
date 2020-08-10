# Minecraft Server VPS Scripts  

#### Running  
Assuming a brand new server  

First things first:  
```sh
# Clone Repo
git clone https://github.com/EniMiniGames/MC-Server-VPS-Scripts.git 
cd MC-Server-VPS-Scripts

# Install Requirements
python3 -m pip install -r requirements.txt

# Copy change config file extensions
# https://unix.stackexchange.com/a/440791/427069
rename 's/\.example.yml$/.yml/' *.example.yml

# Fill out config options in digitalocean_config.yml [See TODO]
```  

## Running  
```sh
# Create new Bungee Server on new VPS
python3 new_bungee {Name, for reference} {Config Definition in digitalocean_config.yml} {OPTIONAL_ARGS}

# Create new server to attach to Bungee
python3 new_server {Name, for reference} {Config Definition in digitalocean_config.yml} -b {Bungee name, as defined in bungee_info.yml} {OPTIONAL_ARGS}
```

#### TODO  

- [ ] Firewalls  
- [ ] Comment scripts  
- [x] spigot.yml, bungeecord: true script
- [x] Bungee config.yml ip_forward: true script
- [x] Use DO API to do all this. Bungee on 512MB server, Lobby on 1GB server, rest on whatever.
- [x] Use DO-API in Bungee plugin to spin up new server for each gamemode.
- [ ] Config options documentation
