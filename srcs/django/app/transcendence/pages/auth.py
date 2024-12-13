from django.contrib.auth.models import User, AnonymousUser
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def logoutUser(request: Request) -> Response:
	logout(request)
	response = render(request, "auth.html")
	response.delete_cookie("access_token")
	response.delete_cookie("session_id")
	return response

def response(request: Request):
	if "logout" in request.query_params:
		return logoutUser(request)
	user: User = request.user
	if not type(user) is AnonymousUser:
		return redirect("/")
	error = ""
	status = 200

	if "error" in request.query_params.keys():
		status = 401
		error = request.query_params["error"]
	return render(request, "auth.html", {"ERROR_MESSAGE": error}, status=status)