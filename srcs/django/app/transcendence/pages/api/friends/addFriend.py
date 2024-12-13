from django.shortcuts import render, redirect
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from database.models import FriendList
from channels.layers import get_channel_layer, BaseChannelLayer

def response(request: Request) -> HttpResponse:
	if "username" not in request.data:
		return redirect("/friends/?error=Invalid body")
	username: str = request.data['username']
	user: User = request.user

	if not User.objects.filter(username=username).exists():
		return redirect(f"/friends/?error=Could not find user.&username={username}")

	friend: User = User.objects.get(username=username)
	if friend.id is user.id:
		return redirect(f"/friends/?error=You cannot add yourself to your friends.&username={username}")

	if FriendList.objects.filter(friend=friend, user=user).exists():
		return redirect("/friends/?error=This user is already in your friends.")
	FriendList.objects.create(user=user, friend=friend)
	friendGroup = f"{friend.username}_notifications"
	layer: BaseChannelLayer = get_channel_layer()
	layer.group_send(friendGroup, {
		"type": "sendMessage",
		"message": "test"
	})
	return redirect("/friends/?success=Friend invitation successfully sent!")