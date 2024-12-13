from django.contrib.auth.models import User
from database.models import FriendList
from rest_framework.request import Request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth")
def response(request: Request):
	if "friendID" not in request.data:
		return redirect("/friends?error=Missing friend ID in request.", status=400)

	friend = User.objects.get(id=request.data["friendID"])
	friendship = FriendList.objects.filter(user=friend, friend=request.user)

	if not friendship.exists():
		return redirect("/friends?error=Failed to find friendship", status=400)

	friendship = FriendList.objects.get(user=friend, friend=request.user)
	friendship.delete()
	return redirect("/friends?error=Rejected friend request successfully")