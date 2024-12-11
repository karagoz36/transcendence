from django.shortcuts import redirect, render
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login

def response(request: Request) -> HttpResponse:
	if "username" not in request.data or "password" not in request.data:
		return redirect("/auth/?error=Missing password or username")
	username: str = request.data['username']
	password: str = request.data['password']
	if User.objects.filter(username=username).exists():
		return redirect("/auth/?register&error=Username already taken")
	user = User.objects.create_user(username, '', password)
	login(request, user)
	return redirect("/")