import json
from django.contrib.auth.models import User
from rest_framework.request import Request
from database.models import getFriendship
from django.shortcuts import redirect
from websockets.consumers import sendMessageWS

async def response(request: Request):
    friend: User
    user: User = request.user

    if user.is_anonymous:
        return redirect("/api/logout")
    if "friendID" not in request.data:
        return redirect("/friends?error=Missing friend ID in request")

    try:
        friend = await User.objects.aget(id=request.data["friendID"])
    except:
        return redirect("/friends?error=Invalid friend ID sent")

    friendship = await getFriendship(user, friend)
    if friendship is None:
        return redirect("/friends?error=This friendship does not exist")

    friendship.invitePending = False
    await friendship.asave()
    message = {"message": f"{user.username} accepted your friend invitation.", "link":"/friends", "refresh": ["/friends/"]}
    await sendMessageWS(friend, "notifications", json.dumps(message))
    return redirect("/friends?success=Friend invite accepted!")