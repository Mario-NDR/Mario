#!/bin/sh
if [ ! -f $(ls /opt/marioips/log | grep update.log) ]
then
        update_time_server=`curl http://remoteadd:5000/api/update?operation=check`
        update_time_client=`sed -n '2p' /opt/marioips/log/update.log`
        if [ "$update_time_server" != 'no update' ] && [ "$update_time_server" != "$update_time_client" ]
        then
            echo `date '+%Y-%m-%d %H:%M:%S'` "upgrade the main program"
            sed -i "2c ${update_time_server}" /opt/marioips/log/update.log
            curl http://remoteadd:5000/install.sh | bash -s update
            rm -rf /opt/marioips/log/pcap_log/*
        else
            echo `date '+%Y-%m-%d %H:%M:%S'` "Don't need to upgrade the main program"
        fi
else
        echo -e "update time\nnever update" > /opt/marioips/log/update.log
        echo `date '+%Y-%m-%d %H:%M:%S'` "first upgrade the main program"
fi
