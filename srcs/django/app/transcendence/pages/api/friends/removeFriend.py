from django.contrib.auth.models import User
from database.models import FriendList, getFriendship
from rest_framework.request import Request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth")
async def response(request: Request):
	user: User = request.user
	friend: User

	if "friendID" not in request.data:
		return redirect("/friends?error=friendID must be present in body request", status=400)

	try:
		friend = await User.objects.aget(id=id)
	except:
		return redirect("/friends?error=Invalid friendID sent", status=400)

	friendship: FriendList = await getFriendship(request.user, friend)
	if friendship is None:
		return redirect("/friends?error=Friendship not found", status=400)

	await friendship.adelete()
	return redirect("/friends?error=Friend successfully removed")