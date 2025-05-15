from django.urls import path
import app1.views as vs


urlpatterns = [
    path('', vs.index, name='index_app1'), # http://127.0.0.1:8000/app1/
    path('users/', vs.index2, name='index2_app1'), # http://127.0.0.1:8000/app1/users/
    path('test/<int:count>/', vs.test, name='test1'), #http://127.0.0.1:8000/app1/test/123/
]