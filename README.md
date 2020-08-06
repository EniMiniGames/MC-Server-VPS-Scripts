# Minecraft Server VPS Scripts  

#### Running  
Assuming a brand new server

```sh  
# Clone Repo
git clone https://github.com/EniMiniGames/MC-Server-VPS-Scripts.git .  

# Move scripts into current working dir
mv MC-Server-VPS-Scripts/*.sh .

# Mark as executable
chmod +x vps_setup.sh screen_start.sh startup_loop.sh  # *.sh  

# Run setup
# Might take a bit to download/install packages, and run BuildTools
./vps_setup.sh   

cd server  

./screen_start  
# And the server should be up!  
```  

To view the server console, do 
`screen -r`  

To exit that hit `Ctrl + A + D` or `Ctrl + A THEN Ctrl + D`  

#### TODO  

- [ ] Firewalls  
