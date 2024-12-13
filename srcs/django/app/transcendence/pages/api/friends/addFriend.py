from django.shortcuts import redirect
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from database.models import FriendList, getFriendship
from websockets.consumers import sendNotification
import json
from django.contrib.auth.decorators import login_required
    

@login_required(login_url="/auth")
async def response(request: Request) -> HttpResponse:
	if "username" not in request.data:
		return redirect("/friends/?error=Invalid body")
	username: str = request.data['username']
	user: User = request.user
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

	message = json.dumps({"message": f"Friend invitation received from {user.username}.", "refresh": "/friends/"})
	await sendNotification(friend, message)
	return redirect("/friends/?success=Friend invitation successfully sent!")