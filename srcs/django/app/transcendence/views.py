from django.shortcuts import render
from django.http import HttpResponse, response

def index(request):
    username = "ketrevis"
    return render(request, "index.html", { "USERNAME": username })
