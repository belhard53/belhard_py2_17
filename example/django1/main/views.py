from django.shortcuts import render, HttpResponse

from .models import Student

from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from typing import Any

# Create your views here.

menu =  [
    {'menu1':"url1"},
    {'menu2':"url2"},
]

def index(r):
    # return HttpResponse("<h1>Академия Ы</h1>")
    return render(r, 'base.html')


def students(r):
    students = Student.objects.all()
    return render(r, 'students.html', context={'students':students})


# на уроке не работала т.к. я был авторизован как админ 😂
@login_required(login_url='/login/')
def student(r, id):
    student = Student.objects.get(id=id)    
    return render(r, 'student.html', context={'student':student})



class StudentsView(ListView):
    model = Student
    template_name = 'students.html'
    context_object_name = 'students'
    
    # для уточнения запроса если нет def get
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Student.objects.filter(name='Вася')
    
    # для добавления в контекст доп данных если нет def get
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context =  super().get_context_data(**kwargs)
    #     context['menu'] = menu
    #     return context
    
    # ---------------------------------------
    # http://127.0.0.1:8000/students2/?f=ася
    def get(self, r, *args, **kwargs):
        f = r.GET.get('f', default='')
        # print(f)
        students = Student.objects.filter(name__contains=f).all()
        return render(r, self.template_name, context={'students':students, 'menu':menu})
    
# LoginRequiredMixin - на уроке не работала т.к. я был авторизован как админ  😂
class StudentView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student.html'          
    slug_url_kwarg = 'name_slug'
    context_object_name = 'student'
    # pk_url_kwarg = 'pk' # т.к. тут slug ссылка по id уже не нужна
    login_url = '/login/'    
        
def login(r):
    return HttpResponse("<h1> ЛОГИН </h1>")