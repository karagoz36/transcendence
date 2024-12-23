from django.contrib.auth.models import User, AnonymousUser
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render
from transcendence.pages.friends import getFriends
from websockets.consumers import sendMessageWS

async def getContext(user: User):
	context = {}
	context["error"] = ""
	context["success"] = ""
	context["friends"] = await getFriends(user)
	return context

async def response(request: Request):
	context = await getContext(request.user)
	status = 200

	if "error" in request.query_params:
		context["error"] = request.query_params["error"]
		status = 401

	if "success" in request.query_params:
		context["success"] = request.query_params["success"]
	return render(request, "play/play.html", status=status, context=context)