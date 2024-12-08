from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def response(request: Request):
    user: User = request.user
    if user.is_active:
        return redirect("/")
    return render(request, "auth.html")