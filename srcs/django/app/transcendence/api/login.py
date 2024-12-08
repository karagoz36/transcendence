from django.shortcuts import render
from django.http.request import HttpRequest

def response(request: HttpRequest):
    error = "Failed to connect"
    return render(request, "index.html", { "ERROR_MESSAGE": error })