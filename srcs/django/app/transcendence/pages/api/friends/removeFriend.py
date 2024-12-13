import json
from django.contrib.auth.models import User
from database.models import FriendList
from rest_framework.request import Request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from websockets.consumers import sendNotification

async def getFriend(id: int) -> User|None:
	friend: User
	try:
		friend = await User.objects.aget(id=id)
		return friend
	except:
		return None

async def getFriendship(user: User, friend: User) -> FriendList|None:
	friendship: FriendList
	try:
		friendship = await FriendList.objects.aget(user=user, friend=friend)
		return friendship
	except:
		pass
	try:
		friendship = await FriendList.objects.aget(user=friend, friend=user)
		return friendship
	except:
		pass
	return None
	
@login_required(login_url="/auth")
async def response(request: Request):
	user: User = request.user
	if "friendID" not in request.data:
		return redirect("/friends?error=friendID must be present in body request", status=400)
	friend: User = await getFriend(request.data["friendID"])
	if friend is None:
		return redirect("/friends?error=Invalid friendID sent", status=400)
	friendship: FriendList = await getFriendship(request.user, friend)
	if friendship is None:
		return redirect("/friends?error=Friendship not found", status=400)
	await friendship.adelete()
	await sendNotification(friend, json.dumps({"message": f"{user.username} declined your friend invitation.", "refresh": "/friends/"}))
	return redirect("/friends?error=Rejected friend request successfully")