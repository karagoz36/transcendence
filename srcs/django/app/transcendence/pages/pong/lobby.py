from rest_framework.request import Request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from websockets.consumers import sendMessageWS
import json
from django.contrib.auth.decorators import login_required
from database.models import getFriendship, FriendList

@login_required(login_url="/api/logout")
async def response(req: Request):
    username = req.query_params.get("opponent")
    if username is None:
        return redirect("/pong/?error=Invalid body", status=401)
    
    user: User = req.user
    if username == user.username:
        return redirect("/pong/?error=You cannot invite yourself", status=401)

    try:
        friend: User = await User.objects.aget(username=username)
    except:
        return redirect("/pong/?error=This user does not exist", status=401)
    friendship: FriendList = getFriendship(user, friend)
    if friendship is None:
        return redirect("/pong/?error=This user is not your friend", status=401)
    message = json.dumps({
        "message": f"<a href=/pong/>{user.username} invites you to play pong</a>",
        "refresh": ["/pong/"]
    })
    await sendMessageWS(friend, "notifications", message)
    return render(req, "pong/lobby.html", context={"opponent": friend})