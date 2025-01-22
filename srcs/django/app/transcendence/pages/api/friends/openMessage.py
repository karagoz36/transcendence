from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from database.models import FriendList, getFriendship, Messages
from websockets.consumers import sendMessageWS
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from database.models import Messages


async def getMessages(friendship: FriendList):
	arr = []
	async for message in Messages.objects.select_related("sender").filter(friendship=friendship).order_by("created_at"):
		arr.append({\
			"text": message.message, 
			"sender": message.sender.username, 
			"created_at": message.created_at,})
	return arr

async def response(request: Request) -> HttpResponse:
	user: User = request.user
	id: int = request.data["friendID"]

	try:
		friend = await User.objects.aget(id=id)
	except:
		return Response({"message": "invalid friend id in request body"}, status=401)
	friendship: FriendList = await getFriendship(user, friend)
	if friendship is None:
		return Response({"message": "friendship not found"}, status=401)

	messageList = await getMessages(friendship)
	return render(request, "friendlist/message-list.html", context={"messages": messageList, "friend":friend })
