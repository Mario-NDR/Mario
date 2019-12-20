FROM co0ontty/ubuntu:16.04
RUN apt update && \
    apt install -y python3 python3-pip git && \
    pip3 install -i https://pypi.doubanio.com/simple/ -r requirement.txt && \
    cd /home && \
    git clone https://github.com/co0ontty/Mario.git && \
    echo "cd /home/Mario && python3 Mario.py web" > /etc/start.sh
CMD [ "sh","-c","/etc/start.sh" ]