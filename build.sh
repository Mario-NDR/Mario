apt install -y nginx python3-pip docker.io docker-compose
pip3 install setuptools-rust
pip3 install -r requirements.txt
docker-compose -f ./docker/docker-compose-mongo.yml up -d
docker-compose -f ./docker/docker-compose-elastic.yml up -d
cp ./ThirPath/web/default /etc/nginx/sites-enabled/
cp -r ./ThirPath/web/cert/ /etc/nginx/
sed -i "s/# Basic Settings/client_max_body_size 200m;/g" /etc/nginx/nginx.conf
tar -zxvf ./ThirPath/web/dist.tar.gz -C /var/www/html/
service nginx restart && cd ./uwsgi && uwsgi uwsgi.ini 
