Deploy Django + Nginx + Gunicorn
Установка Nginx на сервер под ОС Ubuntu
sudo apt install nginx
Настройка Django + Gunicorn
1. Подготовка проекта
1. Сменить STATICFILES_DIRS на STATIC_ROOT = os.path.join(BASE_DIR, «static/»)
2. Собрать статические файлы в STATIC_ROOT python manage.py collectstatic
3. Выставить DEBUG = False
4. Прописать хосты, с которых будут происходить запросы в ALLOWED_HOSTS

2. Установить gunicorn в виртуальное окружение с проектом django
pip install gunicorn
3. Проверка возможности обслуживания проекта с помощью gunicorn
gunicorn —bind 0.0.0.0:8000 project.wsgi
4. Создать файл socket
sudo vim /etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/gunicorn.sock
[Install]
WantedBy=sockets.target
5. Создать файле service
sudo /vim/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
[Service]
User=username
Group=www-data
WorkingDirectory=/home/username/myprojectdir
ExecStart=/home/username/myprojectdir/myprojectenv/bin/gunicorn \
--access-logfile - \
--workers 3 \
--bind unix:/run/gunicorn.sock \
project.wsgi:application
[Install]
WantedBy=multi-user.target

6. Активация сервиса
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
7. Проверка работоспособности
curl --unix-socket /run/gunicorn.sock localhost
8. Конфигурация Nginx
sudo vim /etc/nginx/sites-available/project
server {
listen 80;
listen [::]:80;
server_name host_or_domain;
location /static/ {
root /home/username/project — указывает путь до папки где лежит папка static
}
location / {
include proxy_params;
proxy_pass http://unix:/run/gunicorn.sock;
}
}
9. Создать символическую ссылку на файл конфигурации
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
10. Настройка Nginx
sudo vim /etx/nginx/nginx.conf
user www-data;
worker_process auto;
pid /run/nginx.pid
include /etc/nginx/modules-enabled/*.conf
events {
worker_connections 1024;
multi_accept on;
}
http {
sendfile on;
tcp_nopush on;
types_hash_max_size 2048;
include /etc/nginx/mime.types;
default_type application/octetpstream;
access_log /val/log/nginx/access.log;
error_log /val/log/nginx/error.log;

gzip on;
gzip_http_version 1.1;
gzip_types text/plain text/css application/json application/javascript text/xml
application/xml application/xml+rss text/javascript;
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
}
11. Перезапуск Gunicorn + Nginx
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
12. Тест конфигурационных файлов Nginx
sudo nginx -t
DONE!