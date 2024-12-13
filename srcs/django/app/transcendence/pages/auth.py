from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def response(request: Request):
	if not request.user is None:
		return redirect("/")
	if "logout" in request.query_params:
		logout(request)
		response = render(request, "auth.html")
		response.delete_cookie("access_token")
		response.delete_cookie("session_id")
		return response
	error = ""
	status = 200

	if "error" in request.query_params.keys():
		status = 401
		error = request.query_params["error"]
	return render(request, "auth.html", {"ERROR_MESSAGE": error}, status=status)