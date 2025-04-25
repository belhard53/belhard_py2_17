
from django.urls import path
# from app1.views import hello3
from .views import hello3, hello4, hello5

urlpatterns = [
    #/app1/
    path('', hello3, name='hello3'),
    path('hello4/', hello4, name='hello4'),
    path('hello5/', hello5, name='hello5'), # перенаправление на hello4
    
]