from django.shortcuts import redirect
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from utils.users import userIsLoggedIn

@authentication_classes([])
@permission_classes([AllowAny])
def response(request: Request) -> HttpResponse:
	if "username" not in request.data or "password" not in request.data:
		return redirect(f"/auth/?error=Missing password or username")
	username = request.data['username']
	password = request.data['password']
	try:
		user = User.objects.get(username=username)
	except:
		return redirect(f"/auth/?logout&error=No account found with this username")

	if userIsLoggedIn(user):
		return redirect(f"/auth/?logout&error=This account is already logged in somewhere else")

	user = authenticate(username=username, password=password)
	if user is None:
		return redirect(f"/auth/?error=Invalid credentials")

	login(request, user)
	return redirect("/")