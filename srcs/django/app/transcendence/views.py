from collections import defaultdict
from typing import DefaultDict, reveal_type
from django.http.request import HttpRequest
from django.shortcuts import render

def index(request: HttpRequest):
    username = ""
    if "username" in request.GET:
        username = request.GET.get('username')
    return render(request, "index.html", { "USERNAME": username })