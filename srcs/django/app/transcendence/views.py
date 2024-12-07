from collections import defaultdict
from typing import DefaultDict, reveal_type
from django.http.request import HttpRequest
from django.shortcuts import render

def index(request: HttpRequest):
    return render(request, "index.html")

def loginRegister(request: HttpRequest):
    error = ""
    print(request.method)
    return render(request, "index.html", { "ERROR_MESSAGE": error })