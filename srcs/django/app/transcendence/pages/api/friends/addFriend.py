from django.shortcuts import redirect
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from database.models import FriendList, getFriendship
from websockets.consumers import sendMessageWS
import json

async def response(request: Request) -> HttpResponse:
	user: User = request.user

	if user.is_anonymous:
		return redirect("/api/logout")

	if "username" not in request.data:
		return redirect("/friends/?error=Invalid body")
	username: str = request.data['username']
	friend: User = None

	try:
		friend: User = await User.objects.aget(username=username)
	except:
		return redirect("/friends/?error=This user does not exist.")

	if friend.id is user.id:
		return redirect(f"/friends/?error=You cannot add yourself to your friends.")

	if await getFriendship(user, friend) is not None:
		return redirect(f"/friends/?error=This friendship already exists.")

	await FriendList.objects.acreate(user=user, friend=friend)

	message = {"message": f"Friend invitation received from {user.username}.", "link":"/friends", "refresh": ["/friends/"]}

	await sendMessageWS(friend, "notifications", json.dumps(message))
	return redirect("/friends/?success=Friend invitation successfully sent!")