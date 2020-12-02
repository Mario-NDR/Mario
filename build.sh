apt install -y nginx python3-pip docker.io
pip3 install -r requirements.txt
pip3 install docker-compose
docker-compose -f ./docker/docker-compose-mongo.yml up -d
cp ./ThirPath/web/default /etc/nginx/sites-enabled/
sed -i "s/# Basic Settings/client_max_body_size 200m;/g" /etc/nginx/nginx.conf
tar -zxvf ./ThirPath/web/dist.tar.gz -C /var/www/html/
service nginx restart && cd ./uwsgi && uwsgi uwsgi.ini 
