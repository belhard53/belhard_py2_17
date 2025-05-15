import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# in SETTINGS
# CELERY_BROKER_URL = "redis://localhost:6379"



# in app 
# myapp/tasks.py

# from celery import shared_task
# @shared_task
# def add(x, y):
#     return x + y 



#Для выполнения асинхронных задач необходимо запускаем Celery worker:
#Это запустит worker, который будет слушать и выполнять асинхронные задачи.
#celery -A myproject worker --loglevel=info

# Можно еще подрубить мониторинг задач и воркеров с flower:
#celery -A myproject flower