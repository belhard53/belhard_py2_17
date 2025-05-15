"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include,  re_path
from main import views
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),    
    
    # старые - на основании функций
    # path('student/<int:id>/', views.student, name='student'),
    # path('students/', views.students, name='students'),
    
    # на основании классов
    path('students/', views.StudentsView.as_view(), name='students'),
    path('student/<slug:name_slug>/', views.StudentView.as_view(), name='student'),    
    path('students/add/', views.StudentAddView.as_view(), name='student_add'),
    # path('students/<int:id>/edit/', views.StudentEditView.as_view(), name='student_edit'),
    path('students/<int:id>/edit/', views.student_edit_view, name='student_edit'),
    
    
    # если нужен кеш - включается или тут или на views декоратором
    #path('courses/', cache_page(60*15)(Courses.as_view()), name='courses',),
    path('courses/', views.Courses.as_view(), name='courses',),    
    path('courses/<int:id>/', views.Show_course.as_view(), name='course',),
    path('courses/add/', views.course_add_view, name='course_add'),
    path('courses/<int:id>/edit/', views.CourseEditView.as_view(), name='course_edit',),
    
    
    path('reg/', views.RegisterUser.as_view(), name='reg',),
    path('login/', views.LoginUser.as_view(), name='login',),
    path('logout/', views.logout_user, name='logout',),
    
    path('app1/', include('app1.urls')), 
    path('api/', include('main.urls_rest')), 
        
    
    
    # -------------- djoser auth token ----
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # http://127.0.0.1:8000/auth/token/login/
    # http://127.0.0.1:8000/auth/token/logout/
    # header authorization: Token 32739b99f062a34f60fba1f52ac18c336e6e1256
    
    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(            
            settings.MEDIA_URL, 
            document_root=settings.MEDIA_ROOT)
