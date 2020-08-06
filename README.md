# Minecraft Server VPS Scripts  

#### Running  
Assuming a brand new server

```sh  
git clone https://github.com/EniMiniGames/MC-Server-VPS-Scripts.git .  
# Only if directory is empty, otherwise remove the '.' and copy files into current directory  
# ls should have the files from the repo in the current working directory  

chmod +x vps_setup.sh screen_start.sh startup_loop.sh  # *.sh  

./vps_setup.sh   

cd server  

./screen_start  
# And the server should be up!  
```  

To view the server console, do 
`screen -r`  

To exit that hit `Ctrl + A + D` or `Ctrl + A THEN Ctrl + D`  
