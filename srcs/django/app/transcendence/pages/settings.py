from django.contrib.auth.models import User
from rest_framework.request import Request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="/auth")
def response(request: Request):
    return render(request, "settings.html")