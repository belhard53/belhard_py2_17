from django.shortcuts import render

# Create your views here.

def index(request):
    # return HttpResponse("Hello DJANGO")
    return render(request, 't2.html', context={'name':'index1'})

def index2(request):
    # return HttpResponse("Hello DJANGO")
    return render(request, 't2.html', context={'name':'index2'})



def test(request, count):
    return render(request, 't2.html', 
                  context={'name':'test', 'count':'_'*count})