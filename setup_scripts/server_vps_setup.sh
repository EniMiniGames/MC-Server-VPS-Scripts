mkdir BuildTools && cd BuildTools

wget -O "BuildTools.jar" https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar


echo "Spigot BuildTools is now downloaded, will be running the Jar file. This takes a while and has a lot of output, which this script is throwing into /dev/null"
echo "Get you a glass of something in the meanwhile."
echo -e "\e[32mBeginning now.\e[0m"
git config --global --unset core.autocrlf
java -jar BuildTools.jar --rev 1.15.2 > /dev/null 2>&1 # version should be var

echo "" 
echo -e "\e[32mBuildTools has finished running, your Jars and classes are availible for your pleasure.\e[0m" 

cd ..
mkdir server

cp BuildTools/spigot-1.15.2.jar server # var

echo "eula=true" > server/eula.txt

mv -t server start_server_screen.sh server_startup_loop.sh