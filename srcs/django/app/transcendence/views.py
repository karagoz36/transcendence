from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import render

def index(request: HttpRequest):
    return render(request, "index.html")

def loginRegister(request: HttpRequest):
    error = "Failed to connect"
    return render(request, "index.html", { "ERROR_MESSAGE": error })