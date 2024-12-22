from django.contrib.auth.models import User, AnonymousUser
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer, BaseChannelLayer

async def closeWebSockets(id: int):
	layer: BaseChannelLayer = get_channel_layer()
	await layer.group_send(f"{id}_notifications", {
		"type": "closeConnection"
	})

async def logoutUser(request: Request) -> Response:
	response = render(request, "auth.html")
	response.delete_cookie("access_token")
	response.delete_cookie("sessionid")
	await closeWebSockets(request.user.id)
	return response

async def response(request: Request):
	if "logout" in request.query_params:
		return await logoutUser(request)
	user: User = request.user
	if not type(user) is AnonymousUser:
		return redirect("/")
	error = ""
	success = ""
	status = 200

	if "error" in request.query_params.keys():
		status = 401
		error = request.query_params["error"]
	if "success" in request.query_params.keys():
		success = request.query_params["success"]
	return render(request, "auth.html", {"ERROR_MESSAGE": error, "SUCCESS_MESSAGE": success}, status=status)