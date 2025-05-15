from rest_framework.response import Response
from .models import Course, Students
from django.forms.models import model_to_dict
from .serializers import CourseSerializer, StudentsSerializer, CourseSerializer_
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import action
# from rest_framework.authentication import TokenAuthentication


# pip install djangorestframework

#JWT -  JSON Web Token
# pip install djoser
# pip install djangorestframework-simplejwt



# v1 ------------------------------------------------
class CourseAPIView(APIView):
    # def get(self, reques):
    #     return Response({'name':'Python','num':'11'})
    
    # def post(self, request):
        # return Response({'name':'JS','num':'22'})


    def get(self, r, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            course = Course.objects.get(pk=pk)
            return Response({'couse':model_to_dict(course)})         
        
        # без сериализатора
        # courses = Course.objects.all().values()
        # return Response({'courses':list(courses)})
        
        # с сериализаторомм
        courses = Course.objects.all()
        return Response({'courses': CourseSerializer_(courses, many=True).data})


    def post(self, r):  
        
        # без сериализатора
        # course = Course.objects.create(
        #     name = r.data['name'],
        #     course_num = r.data['num'],
        #     description = r.data['descr']
        # )
        
        # return Response(
        #     {'couse':model_to_dict(course)}            
        # )
        
        # c сериализатором
        sr = CourseSerializer_(data=r.data)
        sr.is_valid(raise_exception=True) # raise_exception формирует правильную ошибку в json
        course = Course.objects.create(**sr.validated_data)
        return Response(
            {'couse': CourseSerializer_(course).data}            
        )

    def put(self, r, *args, **kwargs):        
        pk = kwargs.get("pk", None)        
        if not pk:
            return Response({"error": "Method PUT not allowed"})
 
        try:
            course = Course.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        print(r.data)
        
        # так же можно подключить вручную сделанный сериалзатор
        # serializer = StudentsSerializer(data=r.data)
        # if not serializer.is_valid():
        #     return Response({"error": "Field is None"})
        #или вручную
        if not r.data.get('name') or not r.data.get('course_num') or not r.data.get('description'):
            return Response({"error": "Field is None"})
        course.name = r.data['name']
        course.course_num = r.data['course_num']
        course.description = r.data['description']        
        course.save() 
        return Response({'couse':model_to_dict(course)}) 
    



# права доступа из джанго
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly ) 

# свои классы доступа
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
    
    
#v2 ---------------------------    
# работает на встроенных классах на основе сериализаторов созданных на основе моделей

# CreateAPIView – создание данных по POST-запросу;
# ListAPIView – чтение списка данных по GET-запросу;
# RetrieveAPIView – чтение конкретных данных (записи) по GET-запросу;
# DestroyAPIView – удаление данных (записи) по DELETE-запросу;
# UpdateAPIView – изменение записи по PUT- или PATCH-запросу;
# ListCreateAPIView – для чтения (по GET-запросу) и создания списка данных (по POST-запросу);
# RetrieveUpdateAPIView – чтение и изменение отдельной записи (GET-, PUT- и PATCH-запросы);
# RetrieveDestroyAPIView – чтение (GET-запрос) и удаление (DELETE-запрос) отдельной записи;
# RetrieveUpdateDestroyAPIView – чтение, изменение и добавление отдельной записи (GET-, PUT-, PATCH- и DELETE-запросы).



class CourseAPIView2(generics.ListCreateAPIView): # GET, POST
    # в settings настраивается пагинация
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseApiUpdate(generics.UpdateAPIView): # PUT, PATCH,
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, )

class CourseApiDetailView(generics.RetrieveUpdateDestroyAPIView): # GET, PUT, PATCH, DELETE,
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)



# v2 - очень избыточен и там много дублируется поэтому можно юзать v3

# v3 v4 -----------------
# v3 - ендпоинты строятся вручную 
# v4 - ендпоинты строятся автоматически
from rest_framework import viewsets


# на моделях
# только для чтения - viewsets.ReadOnlyModelViewSet
# в urls в скобочках указывает какой метод с какой функцией связан - 
# к примеру {'get':'list','post':'create'}
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    
    # djoser - только по токенам
    # authentication_classes = (TokenAuthentication)
    
    
    # можно добавить доп маршрут /courses/
    # будет работать только на api/v4/students/courses/
    @action(methods=['get'], detail=False)
    def courses(self, request, pk=None):
        course = Course.objects.all()
        return Response({'courses':[f"{c.name}-{c.course_num}" for c in course]})

    # # можно вручную переписать запрос
    # def get_queryset(self):
    #     return Students.objects.all()[:3]

    
    # # можно вручную переписать разные методы
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    
    
# вручную 
class GradeViewSet(viewsets.ViewSet):
    def list(self, request):
        pass
    def create(self, request):
        pass
    def retrieve(self, request, pk=None):
        pass
    def update(self, request, pk=None):
        pass
    def partial_update(self, request, pk=None):
        pass
    def destroy(self, request, pk=None):
        pass