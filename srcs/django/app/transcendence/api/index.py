from django.http.request import HttpRequest
from django.shortcuts import render

def response(request: HttpRequest):
    return render(request, "index.html")