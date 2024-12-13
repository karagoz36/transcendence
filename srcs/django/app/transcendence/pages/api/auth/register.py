from django.shortcuts import redirect, render
from rest_framework.request import Request
from rest_framework.authentication import SessionAuthentication
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes

@authentication_classes([])
@permission_classes([AllowAny])
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