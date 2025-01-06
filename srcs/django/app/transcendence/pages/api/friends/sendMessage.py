from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from database.models import FriendList, getFriendship, Messages
from websockets.consumers import sendMessageWS
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

async def getMessages(friendship: FriendList):
	arr = []

	async for message in Messages.objects.select_related("sender").filter(friendship=friendship).order_by("created_at"):
		arr.append({"text": message.message, "sender": message.sender.username})
	return arr

async def sendNewMessageToFriend(sender: User, receiver: User, message: str):
	context = {}
	context["message"] = {"sender": sender.username, "text": message}
	html = render_to_string("friendlist/message.html", context=context)
	await sendMessageWS(receiver, "messages", html)

async def response(request: Request) -> HttpResponse:
	user: User = request.user

	if user.is_anonymous:
		return redirect("/api/logout")
	if "friendID" not in request.data:
		return Response({"message": "friend id missing in request body"}, status=401)
	if "message" not in request.data or request.data["message"].strip() == "":
		return Response({"message": "message missing in request body"}, status=401)
	if request.data["message"].strip() == "":
		# return Response({"message": "message missing in request body"}, status=401)
		return redirect("/friends/?error=This friendship already exists.")
	print("Requête reçue :", request.data)
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

	friend: User = friendship.friend
	if friend.id == user.id:
		friend = friendship.user
	await sendNewMessageToFriend(user, friend, message)
	return render(request, "friendlist/message-list.html", context={"messages": messageList })
