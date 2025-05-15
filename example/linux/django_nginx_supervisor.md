## Quickstart

Run the following commands to your environment:
    
    sudo apt get update
    sudo apt-get install -y git python3-dev python3-venv python3-pip supervisor nginx vim libpq-dev
    git clone https://github.com/belhard53/django.git
    cd django
      
    python3 -m venv venv   
    source venv/bin/activate
    pip3 install -r requirements.txt 

Migrations:
    python3 manage.py makemigrations
    python3 manage.py migrate
    
Run the app locally:
    python3 manage.py runserver 0.0.0.0:8000 

Run the app with gunicorn:
    gunicorn setting.wsgi -b 0.0.0.0:8000
    
Collect static files:
    
    append to settings.py:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')    
    
    python3 manage.py collectstatic 
    

### Setup NGINX:

    sudo vim /etc/nginx/sites-enabled/default
    
Config file:

    server {
            listen 80 default_server;
            listen [::]:80 default_server;

            location /static/ {
                alias /home/user/django/static/; 
            }

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_redirect off;
                add_header P3P 'CP="ALL DSP COR PSAa OUR NOR ONL UNI COM NAV"';
                add_header Access-Control-Allow-Origin *;
            }
    }
    
Restart NGINX:    
    sudo service nginx restart
    
    
### Setup Supervisor:

    cd /etc/supervisor/conf.d/
    sudo vim django.conf
    
Config file:
    
    [program:django]
    command = /home/user/django/venv/bin/gunicorn setting.wsgi  -b 127.0.0.1:8000 -w 4 --timeout 90
    autostart=true
    autorestart=true
    directory=/home/user/django 
    stderr_logfile=/var/log/my_django_app.err.log
    stdout_logfile=/var/log/my_django_app.out.log
    
Update supervisor with the new process:
    
    sudo supervisorctl reread
    sudo supervisorctl update
    
To restart the process after the code updates run:

    sudo supervisorctl restart django




    
   

