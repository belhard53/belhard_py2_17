from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import StudentAddForm, CourseAddForm, CourseAddForm2, RegisterUserForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView

from django.views.decorators.cache import cache_page



def index(request):
    # return HttpResponse("Hello DJANGO")    
    return render(request, 'main1.html',)


menu =  [
    {'menu1':"url1"},
    {'menu2':"url2"},
]
    
    
# @cache_page(60*15)
# def student(r, id):    
#     # student = Students.objects.get(id=id)
#     student =   get_object_or_404(Students, id=id)   
#     return render(r, 'student.html', context={'student':student})

# def students(r):    
#     students = Students.objects.all()
#     return render(r, 'students.html', context={'students':students, 'menu':menu})


    
    
class StudentsView(ListView):
    model = Students
    template_name = 'students.html'
    context_object_name = 'students'
    
    
    # для уточнения запроса если нет def get
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Students.objects.filter(name='Вася')
    
    
    # для добавления в контекст доп данных если нет def get
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context =  super().get_context_data(**kwargs)
    #     context['menu'] = menu
    #     return context
    
    
    # взять параметры из пути get-запроса
    # http://127.0.0.1:8000/students/?f=11
    # отобразит только тех у кого в имени есть 11
    # def get(self, r, *args, **kwargs):
    #     f = r.GET.get('f', default='')
    #     print(f)
    #     students = Students.objects.filter(name__contains=f).all()
    #     return render(r, 'students.html', context={'students':students, 'menu':menu})

        
class StudentView(DetailView):
          model = Students
          template_name = 'student.html'          
          slug_url_kwarg = 'name_slug'
          context_object_name = 'student'
        #   pk_url_kwarg = 'id'
          

class StudentAddView(LoginRequiredMixin, CreateView): # login дб первый
    form_class = StudentAddForm
    template_name = 'student_add_form.html'
    success_url = reverse_lazy('students')
    login_url = '/login/'
    
    

class StudentEditView(UpdateView):
    model = Students
    fields = '__all__'
    pk_url_kwarg = 'id'


@login_required(login_url='/login/')
def student_edit_view(r, id):    
    student = get_object_or_404(Students, id=id)    
    if r.method=='GET':        
        return render(
                    request=r, 
                    template_name='student_edit_form.html', 
                    context={'form':StudentAddForm(instance=student), 'id':id})
    
    form = StudentAddForm(r.POST, instance=student)
    if form.is_valid(): 
        print(form.cleaned_data)
        form.save()
        return redirect('students')   
    form.add_error(None, "Ошибка....")
    return render(r, 'student_edit_form.html', {'form':form}) 


class Courses(ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'courses' # или #object_list

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context =  super().get_context_data(**kwargs)
    #     context['menu'] = ['menu1', 'menu2']
    #     return context
    
    # def get_queryset(self) -> QuerySet[Any]:
    #     return Course.objects.filter(id=56)
    
class Show_course(DetailView):
    model = Course
    template_name = 'course.html'
    pk_url_kwarg = 'id'
    

class CourseEditView(UpdateView):
    model = Course
    template_name = 'course_add_form.html'
    pk_url_kwarg = 'id'
    fields = '__all__'
    
    
@login_required(login_url='/login/')
def course_add_view(r):
    if r.method == 'POST':
        form = CourseAddForm(r.POST)
        if form.is_valid(): 
            
            # если форма основана на модели
            # form.save()
            # return redirect('students')
            
            
            # без модели
            try:           
                Course.objects.create(**form.cleaned_data)
                return redirect('courses')
            except Exception as e:
                print(e)
                form.add_error(None, "Ошибка>.....")
            
            
    else:
        form = CourseAddForm()
    return render(r, 'course_add_form.html', {'form':form})
        


class RegisterUser(CreateView):
    form_class = RegisterUserForm #UserCreationForm - джанговская формма
    template_name = 'reg.html'
    # success_url = reverse_lazy('login') # для входа сайта
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

    
    
class LoginUser(LoginView):
    form_class = AuthenticationForm 
    template_name = 'login.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('index')

    
    
def logout_user(r):
    logout(r)
    return redirect('login')

def login_user(r):
    return render(r, 'login.html')

def reg_user(r):
    return render(r, 'reg.html')