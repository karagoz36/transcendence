from django.shortcuts import render, redirect
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login

def response(request: Request) -> HttpResponse:
    if "username" not in request.data or "password" not in request.data:
        return render(request, "auth.html", { "ERROR_MESSAGE": "Invalid payload." }, status=400)

    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is None:
        return render(request, "auth.html", { "ERRORMESSAGE": "Invalid credentials." }, status=401)

    login(request, user)
    return redirect("/")