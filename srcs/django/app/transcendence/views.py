from django.shortcuts import render
from django.http import HttpResponse, response

def index(request):
    return HttpResponse(b"Hello world")

# def index(request):
#     return render(request, "index.html")
