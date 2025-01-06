from django.shortcuts import redirect, render
from rest_framework.request import Request
from rest_framework.authentication import SessionAuthentication
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes

def usernamePolicy(username: str) -> str:
	MINIMUM_USERNAME_LEN = 5

	if len(username) < MINIMUM_USERNAME_LEN:
		return f"Username must at least {MINIMUM_USERNAME_LEN} characters long."
	return ""

def passwordPolicy(password: str) -> str:
	MINIMUM_PASSWORD_LEN = 8
 
	if len(password) < MINIMUM_PASSWORD_LEN:
		return f"Password must at least {MINIMUM_PASSWORD_LEN} characters long."
	return ""

@authentication_classes([])
@permission_classes([AllowAny])
def response(request: Request) -> HttpResponse:
	if "username" not in request.data or "password" not in request.data:
		return redirect("/auth/?error=Missing password or username")
	username: str = request.data['username']
	err: str = usernamePolicy(username)
	if err != "":
		return redirect(f"/auth/?register&error={err}")
 
	password: str = request.data['password']
	err = passwordPolicy(password)
	if err != "":
		return redirect(f"/auth/?register&error={err}")

	if username == password:
		return redirect(f"/auth/?register&error=Username and password cannot be the same")
 
	if User.objects.filter(username=username).exists():
		return redirect("/auth/?register&error=Username already taken")

	user = User.objects.create_user(username, '', password)
	return redirect("/auth/?success=Account successfully created")