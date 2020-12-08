cd ../
docker rm -f $(docker ps -aq)
uwsgi --stop Mario/uwsgi/uwsgi.pid
mv Mario/docker/ ./
cp Mario/ThirPath/marioips/rules/local.rules ./agentall.rules
rm -rf Mario/
git clone https://github.com/Mario-NDR/Mario.git
cd Mario/
rm -rf docker
mv ../docker ./
bash build.sh
mv ../agentall.rules ./ThirPath/marioips/rules/local.rules
