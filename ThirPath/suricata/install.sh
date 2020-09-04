if [ ! -n "$1" ] ;then
    echo -e "\033[32m If you run server with docker , please use [curl ip:5000/install.sh | bash -s ip] \033[0m"
    echo -e "\033[32m -------------------------------------------------- \033[0m"
    echo -e "\033[32m | Install suricata and Depend on the environment  | \033[0m"
    echo -e "\033[32m -------------------------------------------------- \033[0m"
    apt update -y && \
    sudo apt-get install software-properties-common -y && \
    sudo add-apt-repository ppa:oisf/suricata-stable -y && \
    apt update -y && \
    apt -y install libpcre3 libpcre3-dbg libpcre3-dev build-essential autoconf automake libtool libpcap-dev libnet1-dev libyaml-0-2 libyaml-dev zlib1g zlib1g-dev libcap-ng-dev libcap-ng0 make libmagic-dev libjansson-dev libjansson4 pkg-config libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev libnfnetlink0 suricata
    if [ $? -eq 0 ]; then
        echo -e "\033[32m -------------------------------------------------- \033[0m"
        echo -e "\033[32m |        Download the configuration file          | \033[0m"
        echo -e "\033[32m -------------------------------------------------- \033[0m"
        wget http://ipadd:5000/marioips.tar.gz
        remoteadd="ipadd"
        if [ $? -eq 0 ]; then
            mkdir /opt/marioips
            tar -zxPf marioips.tar.gz -C /opt/marioips/
            sed -i "s/remoteadd/$remoteadd/g" /opt/marioips/bin/senteve.sh
            sed -i "s/remoteadd/$remoteadd/g" /opt/marioips/bin/repost.sh
            sed -i "s/remoteadd/$remoteadd/g" /opt/marioips/bin/update.sh
            cp /opt/marioips/bin/mario.service /etc/systemd/system/
            cp /opt/marioips/bin/mariosent.service /etc/systemd/system/
            mkdir /opt/marioips/log/
            mkdir /opt/marioips/log/post_error/
            mkdir /opt/marioips/log/post_success/
            rm -rf marioips.tar.gz
            systemctl enable mario
            systemctl enable mariosent
            systemctl start mario
            echo -e "\033[32m -------------------------------------------------- \033[0m"
            echo -e "\033[32m |               start ips mode                     | \033[0m"
            echo -e "\033[32m -------------------------------------------------- \033[0m"
            sleep 10s
            systemctl start mariosent
        else
            echo -e "\033[31m can you connect to Mario server ? \033[0m"
        fi
    else
        echo -e "\033[31m Please check your apt environment \033[0m"
    fi
else
    if [ "$1" != "update" ];then
        wget http://$1:5000/marioips.tar.gz
        remoteadd=$1
    else
        echo -e "\033[32m The main program to upgrade \033[0m" 
        wget http://ipadd:5000/marioips.tar.gz
        remoteadd="ipadd"
        tar -zxPf marioips.tar.gz -C /opt/marioips/
        sed -i "s/remoteadd/$remoteadd/g" /opt/marioips/bin/senteve.sh
        sed -i "s/remoteadd/$remoteadd/g" /opt/marioips/bin/repost.sh
        sed -i "s/remoteadd/$remoteadd/g" /opt/marioips/bin/update.sh
        cp /opt/marioips/bin/mario.service /etc/systemd/system/
        cp /opt/marioips/bin/mariosent.service /etc/systemd/system/
        rm -rf marioips.tar.gz
        rm -rf /opt/marioips/log/post_success/*
        rm -rf /opt/marioips/log/post_error/*
        systemctl enable mario
        systemctl enable mariosent
        systemctl restart mario
        echo -e "\033[32m Waiting for the connection \033[0m" 
        sleep 10s
        systemctl restart mariosent
        echo "upgrade success"
    fi
fi
