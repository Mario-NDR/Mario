FROM co0ontty/ubuntu:16.04

COPY ./ /Mario/

RUN apt update && \
    apt install -y python3 python3-pip git curl nginx && \
    cp /Mario/ThirPath/web/default /etc/nginx/sites-enabled/ && \
    tar -zxvf /Mario/ThirPath/web/dist.tar.gz -C /var/www/html/ && \
    pip3 install -i https://pypi.doubanio.com/simple/ -r /Mario/requirements.txt && \
    echo "service nginx restart && cd /Mario/uwsgi && uwsgi uwsgi.ini && tail -f /var/log/nginx/access.log" > /etc/start.sh && \
    chmod +x /etc/start.sh

CMD [ "sh","-c","/etc/start.sh" ]
