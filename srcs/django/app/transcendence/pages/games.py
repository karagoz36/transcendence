from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models import FriendList
from utils.friends import userToDict, getFriends
from django.contrib.auth.decorators import login_required

@login_required(login_url="/api/logout")
async def response(request: Request) -> HttpResponse:
    user: User = request.user
    if user.is_anonymous:
        return redirect("/api/logout")
    status = 200
    err = ""
    success = ""
 
    if "error" in request.query_params:
        status = 401
        err = request.query_params["error"]
    if "success" in request.query_params:
        success = request.query_params["success"]
    return render(request, "games.html", status=status)
