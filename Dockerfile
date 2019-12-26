FROM co0ontty/ubuntu:16.04
RUN apt update && \
    apt install -y python3 python3-pip git curl && \
    git clone https://github.com/co0ontty/Mario.git && \
    pip3 install -i https://pypi.doubanio.com/simple/ -r /Mario/requirements.txt && \
    echo "cd /Mario && python3 Mario.py web" > /etc/startmario.sh
RUN curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh && \
    chmod +x nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get install -y nodejs && \
    git clone https://github.com/xiaosongshua/design_UI.git && \
    cd /design_UI && npm install && \
    echo "cd /design_UI && npm start" > /etc/startui.sh && \
    echo "nohup /etc/startmario.sh & \n sh /etc/startui.sh" > /etc/start.sh && \
    chmod +x /etc/startmario.sh /etc/startui.sh /etc/start.sh
CMD [ "sh","-c","/etc/start.sh" ]
