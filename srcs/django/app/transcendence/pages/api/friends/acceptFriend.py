from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def response(request: Request):
    return redirect("/friends?success=Friend invite accepted!")