service mario stop
service mariosent stop
rm -rf /opt/marioips/
rm -rf /etc/systemd/system/mario.service
rm -rf /etc/systemd/system/mariosent.service