from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from database.models import FriendList
from channels.layers import get_channel_layer, BaseChannelLayer
from rest_framework_simplejwt.tokens import AccessToken

def response(request: Request) -> HttpResponse:
	return render(request, "friendlist/friendlist.html",
		{"friends": request.user.friends.all(), "friendOf": request.user.friendOf.all()})