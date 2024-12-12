from django.shortcuts import render, redirect
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.authentication import JWTAuthentication

def response(request: Request) -> HttpResponse:
	if "username" not in request.data or "password" not in request.data:
		return redirect(f"/auth?error=Missing password or username")
	user = authenticate(username=request.data['username'], password=request.data['password'])
	if user is None:
		return redirect(f"/auth?error=Invalid credentials")
	login(request, user)
	return redirect("/")