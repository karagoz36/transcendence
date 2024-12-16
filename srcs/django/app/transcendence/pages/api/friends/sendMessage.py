from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from database.models import FriendList, getFriendship, Messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from asgiref.sync import sync_to_async

async def getMessages(friendship: FriendList):
	arr = []
	async for message in Messages.objects.select_related("sender").filter(friendship=friendship):
		arr.append({"text": message.message, "sender": message.sender.username})
	arr.reverse()
	return arr

@login_required(login_url="/auth")
async def response(request: Request) -> HttpResponse:
	user: User = request.user

	if "friendID" not in request.data:
		return Response({"message": "friend id missing in request body"}, status=401)
	if "message" not in request.data:
		return Response({"message": "message missing in request body"}, status=401)

	message: str = request.data["message"]
	id: int = request.data["friendID"]

	try:
		friend = await User.objects.aget(id=id)
	except:
		return Response({"message": "invalid friend id in request body"}, status=401)

	friendship: FriendList = await getFriendship(user, friend)
	if friendship is None:
		return Response({"message": "friendship not found"}, status=401)

	await Messages.objects.acreate(friendship=friendship, message=message, sender=user)
	messageList = await getMessages(friendship)
	return render(request, "friendlist/messages.html", context={"messages": messageList })