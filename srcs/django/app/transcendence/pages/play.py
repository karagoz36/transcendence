from django.contrib.auth.models import User, AnonymousUser
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render
from transcendence.pages.friends import getFriends
from websockets.consumers import sendMessageWS

def getContext(request: Request):
	context = {}
	context["error"] = ""
	context["success"] = ""
	context["friends"] = getFriends(request)
	return context

def response(request: Request):
	context = getContext(request)
	status = 200

	if "error" in request.query_params:
		context["error"] = request.query_params["error"]
		status = 401

	if "success" in request.query_params:
		context["success"] = request.query_params["success"]
	return render(request, "play/play.html", status=status, context=context)