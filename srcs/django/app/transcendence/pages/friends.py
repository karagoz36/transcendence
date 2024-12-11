from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models import FriendList

def response(request: Request) -> HttpResponse:
	return render(request, "friendlist/friendlist.html",
		{"friends": request.user.friends.all(), "friendOf": request.user.friendOf.all()})