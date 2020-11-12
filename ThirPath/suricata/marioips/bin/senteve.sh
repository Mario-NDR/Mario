#!/bin/sh
while true;do
	bash /opt/marioips/bin/repost.sh
	wget http://remoteadd:5000/local.rules -O /opt/marioips/rules/local.rules
	newfile="eve_`date '+%Y%m%d%H%M%S'`.json"
	newpcap_file="eve_`date '+%Y%m%d%H%M%S'`.pcap"
	bash /opt/marioips/bin/update.sh
	if [ $(ls /opt/marioips/log/post_success/ | wc -l) -ge 10 ];
	then
		rm -rf $(ls /opt/marioips/log/post_success/ | sort -n | sed -n '10p')
	fi
	service mario stop
	mv /opt/marioips/log/eve.json /opt/marioips/log/$newfile
	mv /opt/marioips/log/marioips.pcap.* /opt/marioips/log/pcap_log/
	if [ $(ls /opt/marioips/log/pcap_log/ |grep pcap | wc -l) -ge 10 ];
	then
		rm -rf $(ls /opt/marioips/log/pcap_log/ |grep pcap | sort -n | sed -n '10p')
	fi
	echo `date '+%Y-%m-%d %H:%M:%S'` "backup eve.json to $newfile"
	check_results=`curl -F "clientfile=@/opt/marioips/log/$newfile" -H "Accept: application/json" http://remoteadd:5000/api/evefile`
	if [[ $check_results =~ "success" ]]
	then
		mv /opt/marioips/log/$newfile /opt/marioips/log/post_success/
		echo `date '+%Y-%m-%d %H:%M:%S'` "post eve.json success"
		rm -rf /opt/marioips/log/fast.log
	else
		mv /opt/marioips/log/$newfile /opt/marioips/log/post_error/
		echo `date '+%Y-%m-%d %H:%M:%S'` "post $newfile error"
	fi
	service mario start
	echo `date '+%Y-%m-%d %H:%M:%S'` "service mario restart"
	sleep 10m;
done