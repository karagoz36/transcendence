from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render

def response(request: Request):
    return render(request, "settings.html")