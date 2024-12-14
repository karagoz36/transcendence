from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from database.models import FriendList
from channels.layers import get_channel_layer, BaseChannelLayer
from rest_framework_simplejwt.tokens import AccessToken

def getInvitesReceived(request: Request):
    res = []
    invitesReceived = FriendList.objects.filter(friend=request.user, invitePending=True)
    for invite in invitesReceived:
        res.append({
            "id": invite.user.id,
            "username": invite.user.username
        })
    return res

def getInvitesSent(request: Request):
    res = []
    invitesSent = FriendList.objects.filter(user=request.user, invitePending=True)
    for invite in invitesSent:
        res.append({
            "id": invite.friend.id,
            "username": invite.friend.username
        })
    return res

def getFriends(request: Request):
    res = []
    friends = FriendList.objects.filter(user=request.user, invitePending=False)
    for friend in friends:
        res.append({
            "id": friend.friend.id,
            "username": friend.friend.username
        })
    friends = FriendList.objects.filter(friend=request.user, invitePending=False)
    for friend in friends:
        res.append({
            "id": friend.user.id,
            "username": friend.user.username
        })
    return res

def response(request: Request) -> HttpResponse:
    invitesReceived = getInvitesReceived(request)
    invitesSent = getInvitesSent(request)
    friends = getFriends(request)
    status = 200
    err = ""
    success = ""
 
    if "error" in request.query_params:
        status = 401
        err = request.query_params["error"]
    if "success" in request.query_params:
        success = request.query_params["success"]
    return render(request, "friendlist/friendlist.html", status=status,
        context={"friends": friends, "invitesReceived": invitesReceived, "invitesSent": invitesSent, "ERROR_MESSAGE": err, "SUCCESS_MESSAGE": success})