from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from database.models import FriendList
from channels.layers import get_channel_layer, BaseChannelLayer
from rest_framework_simplejwt.tokens import AccessToken

async def getInvitesReceived(request: Request):
    res = []
    invitesReceived = FriendList.objects.select_related("user").filter(friend=request.user, invitePending=True)

    async for invite in invitesReceived:
        res.append({
            "id": invite.user.id,
            "username": invite.user.username
        })
    return res

async def getInvitesSent(request: Request):
    res = []
    invitesSent = FriendList.objects.select_related("friend").filter(user=request.user, invitePending=True)

    async for invite in invitesSent:
        res.append({
            "id": invite.friend.id,
            "username": invite.friend.username
        })
    return res

async def getFriends(request: Request):
    res = []

    friends = FriendList.objects.select_related("friend").filter(user=request.user, invitePending=False)
    async for friend in friends:
        res.append({
            "id": friend.friend.id,
            "username": friend.friend.username
        })
    friends = FriendList.objects.select_related("user").filter(friend=request.user, invitePending=False)
    async for friend in friends:
        res.append({
            "id": friend.user.id,
            "username": friend.user.username
        })
    return res

async def getContext(request: Request, err: str, success: str) -> dict:
    context = {}
    context["friends"] = await getFriends(request)
    context["invitesReceived"] = await getInvitesReceived(request)
    context["invitesSent"] = await getInvitesSent(request)
    context["ERROR_MESSAGE"] = err
    context["SUCCESS_MESSAGE"] = success
    context["showModal"] = "show"
    return context

async def response(request: Request) -> HttpResponse:
    status = 200
    err = ""
    success = ""
 
    if "error" in request.query_params:
        status = 401
        err = request.query_params["error"]
    if "success" in request.query_params:
        success = request.query_params["success"]
    context = await getContext(request, err, success)
    return render(request, "friendlist/friendlist.html", status=status, context=context)