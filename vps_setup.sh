apt update
apt install wget screen default-jdk -y

mkdir BuildTools && cd BuildTools

wget -O "BuildTools.jar" https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar


git config --global --unset core.autocrlf

java -jar BuildTools.jar --rev 1.15.2 > /dev/null 2>&1 # version should be var

cd ..
mkdir server

cp BuildTools/spigot-1.15.2.jar server # var

echo "eula=true" > server/eula.txt

mv -t server screen_start.sh startup_loop.sh