from django.contrib.auth.models import User
from database.models import FriendList
from rest_framework.request import Request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def getFriend(id: int) -> User|None:
	friend: User
	try:
		friend = User.objects.get(id=id)
	except:
		return None
	return friend

def getFriendship(user: User, friend: User) -> FriendList|None:
	friendship: FriendList
	try:
		friendship = FriendList.objects.get(user=user, friend=friend)
		print(friendship)
		return friendship
	except:
		pass
	try:
		friendship = FriendList.objects.get(user=friend, friend=user)
		print(friendship)
		return friendship
	except:
		pass
	return None
	

@login_required(login_url="/auth")
def response(request: Request):
	if "friendID" not in request.data:
		return redirect("/friends?error=friendID must be present in body request", status=400)

	friend: User = getFriend(request.data["friendID"])
	if friend is None:
		return redirect("/friends?error=Invalid friendID sent", status=400)
	friendship: FriendList = getFriendship(request.user, friend)
	if friendship is None:
		return redirect("/friends?error=Friendship not found", status=400)
	friendship.delete()
	return redirect("/friends?error=Rejected friend request successfully")