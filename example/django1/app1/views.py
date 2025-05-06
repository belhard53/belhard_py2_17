from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse


from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
"""
HttpResponsePermanentRedirect отличается от HttpResponseRedirect только статус-кодом HTTP-ответа:

HttpResponseRedirect возвращает статус-код 302 (Found), что означает временное перенаправление. 
        Браузеры и поисковые системы понимают, что ресурс может быть перемещён только на время, 
        и не должны обновлять закладки или индексацию.
HttpResponsePermanentRedirect возвращает статус-код 301 (Moved Permanently), что означает 
        постоянное перенаправление. Это сигнал для браузеров и поисковых систем, что адрес 
        изменился навсегда, и следует обновить закладки, а поисковики — переиндексировать новый адрес
"""

# Create your views here.

def index(request):
    return HttpResponse("<h1>Hello INDEX</h1>")
    
def hello2(request, num=1):
    html = ''
    for i in range(num):
            html += "<h1>Hello2</h1>"
    return HttpResponse(html)
    
def hello3(request):
    return HttpResponse(f"<h1>Hello3</h1>")


def hello4(request):    
    return HttpResponse("<h1>Hello4</h1>")

def hello5(request):    
    # перенаправление на hello4
    return redirect("hello4") # по имени - самый лаконичный вариант
    # return redirect("/app1/hello4/") # по прямому пути
    # или аналогично
    # return HttpResponseRedirect(reverse("hello4")) # по имени 
    # return HttpResponseRedirect("/app1/hello4/") # по прямому пути

def user_num(request, name='', num=0):
    html = f'''
    <h1> Пользователь {name}, номер {num}</h1>    
    '''
    return HttpResponse(html)

def data_year(request, year):
    if 2000 <= int(year) <= 2025:        
        html = f'''
        <h1> Данные  за {year} год.</h1>    
        '''
        return HttpResponse(html)
    return HttpResponse("Нет данных за этот год")    

def user_info(request, name, age): 
    return HttpResponse(f"Name: {name}, Age: {age}")

def multi_path(request, path):
    return HttpResponse(f"вы попали на {path}")

def users(r):
    a = 1
    users = ['user1', 'user2', 'user3', 'user4']
    return render(r, 'users.html', context={'users':users, "var":a, "var2":12345} )