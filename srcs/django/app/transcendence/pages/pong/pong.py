from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render
from transcendence.pages.friends import getFriends
from django.contrib.auth.decorators import login_required

async def getOnlineFriends(user: User):
	loggedInFriends = []
	friends = await getFriends(user)

	for friend in friends:
		if friend["status"] == "online":
			loggedInFriends.append(friend)
	return loggedInFriends

async def getContext(user: User):
	context = {}
	context["error"] = ""
	context["success"] = ""
	context["friends"] = await getOnlineFriends(user)
	return context

@login_required(login_url="/api/logout")
async def response(request: Request):
	context = await getContext(request.user)
	status = 200

	if "error" in request.query_params:
		context["error"] = request.query_params["error"]
		status = 401
	if "success" in request.query_params:
		context["success"] = request.query_params["success"]
	return render(request, "pong/index.html", status=status, context=context)