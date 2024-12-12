from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def response(request: Request):
	logout(request)
	error = ""
	status = 200

	if "error" in request.query_params.keys():
		status = 401
		error = request.query_params["error"]
	return render(request, "auth.html", {"ERROR_MESSAGE": error}, status=status)