"""
URL configuration for setting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
# from app1.views import index, hello2, hello3, user_num
# from app1 import views
from app1.views import *


urlpatterns = [
    path('', index, name='index'),
    
    path('users/', users, name='users'),
    
    # other path
    path('hello2/', hello2, name='hello2'),
    path('hello3/', hello3, name='hello3'),    
   
    # с указанием до параметра
    # напечатает hello количество раз num
    path('hello2/<int:num>/', hello2, name='hello2__num'), 
    
    # hello10 - 10 будет параметром
    # напечатает hello количество раз num
    path('hello<int:num>/', hello2, name='hello2_num'), 
    
    # /user/vasya-11/
    # любое имя и любое число через дефис
    path('user/<str:name>-<int:num>/', user_num, name='user_num'), 
    
    # передать параметры вручную
    path('user_info/', user_info, kwargs={"name": "Tom", "age": 38}),
    
    #регулярные выражения - 4 цифры подряд - /data/2004/
    # re_path(r'^data/(?P<year>[0-9]{4})/$', data_year, name='data_year'), 
    re_path(r'^data/(?P<year>\d{4})/$', data_year, name='data_year'), 
    
    # несколько вариантов в один path
    # /path1/ или /path2/ или /path3/
    re_path(r'^(path1|path2|path3)/$', multi_path, name='multi_path'),
    
    
    # app1
    path('app1/', include('app1.urls')),
    
    # админка - несколько путей могут вести к одному обработчику        
    path('admin/', admin.site.urls),
    path('adminka/', admin.site.urls),
    path('adminushka/', admin.site.urls),
       
]


"""
ТИПЫ ПАРАМЕТРОВ
str — любая непустая строка без символа /
int — положительное целое число
slug — буквы, цифры, дефисы и подчёркивания
uuid — UUID
path — строка, может содержать символ /"""
