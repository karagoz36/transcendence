from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/api/logout")
def response(request: Request):
    return render(request, "settings.html")