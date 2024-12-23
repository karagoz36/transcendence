from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from database.models import FriendList
from django.contrib.auth.decorators import login_required

def userToDict(user: User) -> dict:
    return {
       "id": user.id,
        "username": user.username,
        "status": "online" if userIsLoggedIn(user) else "offline",
        }

async def getInvitesReceived(user: User):
    res = []
    invitesReceived = FriendList.objects.select_related("user").filter(friend=user, invitePending=True)

    async for invite in invitesReceived:
        res.append(userToDict(invite.user))
    return res

async def getInvitesSent(user: User):
    res = []
    invitesSent = FriendList.objects.select_related("friend").filter(user=user, invitePending=True)

    async for invite in invitesSent:
        res.append(userToDict(invite.friend))
    return res

async def getFriends(user: User):
    res = []

    friends = FriendList.objects.select_related("friend").filter(user=user, invitePending=False)
    async for friend in friends:
        res.append(userToDict(friend.friend))

    friends = FriendList.objects.select_related("user").filter(friend=user, invitePending=False)
    async for friend in friends:
        res.append(userToDict(friend.user))
    return res

async def getContext(user: User, err: str, success: str) -> dict:
    context = {}
    context["friends"] = await getFriends(user)
    context["invitesReceived"] = await getInvitesReceived(user)
    context["invitesSent"] = await getInvitesSent(user)
    context["ERROR_MESSAGE"] = err
    context["SUCCESS_MESSAGE"] = success
    context["showModal"] = "show"
    return context

@login_required(login_url="/api/logout")
async def response(request: Request) -> HttpResponse:
    status = 200
    err = ""
    success = ""
 
    if "error" in request.query_params:
        status = 401
        err = request.query_params["error"]
    if "success" in request.query_params:
        success = request.query_params["success"]
    context = await getContext(request.user, err, success)
    return render(request, "friendlist/friendlist.html", status=status, context=context)

from websockets.consumers import userIsLoggedIn