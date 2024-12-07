from collections import defaultdict
from typing import DefaultDict, reveal_type
from django.http.request import HttpRequest
from django.shortcuts import render
import os

def index(request: HttpRequest):
    return render(request, "index.html")

def loginRegister(request: HttpRequest):
    error = "Failed to connect"
    return render(request, "index.html", { "ERROR_MESSAGE": error })