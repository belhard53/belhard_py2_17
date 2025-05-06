from django.shortcuts import render, HttpResponse
from .models import Student
# Create your views here.


def index(r):
    # return HttpResponse("<h1>Академия Ы</h1>")
    return render(r, 'base.html')

def students(r):
    students = Student.objects.all()
    return render(r, 'students.html', context={'students':students})


def student(r, id):
    student = Student.objects.get(id=id)    
    return render(r, 'student.html', context={'student':student})