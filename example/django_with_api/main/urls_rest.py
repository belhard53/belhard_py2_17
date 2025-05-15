from django.urls import path, include
from .views_rest import *
from rest_framework import routers

# нужны для v4 - что бы он сам построил все ендпоинты
# router = routers.SimpleRouter() 
# http://127.0.0.1:8000/api/v4/
router = routers.DefaultRouter() # добавляет ендпоинт api/v4/ в котором показывает существующие ендпоинты
router.register(r'students', StudentsViewSet)
router.register(r'courses', CourseViewSet)


urlpatterns = [
    path('v1/courses/', CourseAPIView.as_view()),
    path('v1/courses/<int:pk>/', CourseAPIView.as_view()),
    
    path('v2/courses/', CourseAPIView2.as_view() ),                 # GET, POST
    path('v2/courses/<int:pk>/', CourseApiUpdate.as_view() ),       # PUT, PATCH, OPTIONS
    path('v2/course/<int:pk>/', CourseApiDetailView.as_view() ),    # GET, PUT, PATCH, DELETE,
    
    path('v3/courses/', CourseViewSet.as_view({'get':'list','post':'create'}) ), # в скобочках метод связывает с нужной функцией
    path('v3/courses/<int:pk>/', CourseViewSet.as_view({'get':'retrieve'}) ),
    path('v3/students/', StudentsViewSet.as_view({'get':'list','post':'create'}) ),
    path('v3/students/<int:pk>/', StudentsViewSet.as_view({'get':'retrieve'}) ),
    
    
    # утентификация на сессиях 
    # в куки попадает id сессии по которой django Проверяет пользователя
    # api/v3/auth/login/
    # api/v3/auth/logout/
    path('v3/auth/', include('rest_framework.urls') ),
    

    #работает на вьюСетах как и v3 но ендпоинты строит сам на основе созданных роутеров
    path('v4/auth/', include('rest_framework.urls') ),
    # http://127.0.0.1:8000/api/v4/
    # http://127.0.0.1:8000/api/v4/courses/
    # http://127.0.0.1:8000/api/v4/students/
    path('v4/', include(router.urls) ),
    
    
    
]