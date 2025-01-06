from rest_framework.request import Request
from django.shortcuts import redirect, render, render
from django.contrib.auth.models import User
from websockets.consumers import sendMessageWS
import json
from database.models import getFriendship
from utils.users import userIsLoggedIn

async def response(req: Request):
    user: User = req.user

    if user.is_anonymous:
        return redirect("/api/logout")

    username = req.query_params.get("opponent")

    if username is None:
        return redirect("/friends/?error=No username passed in parameter", status=401)
    
    if username == user.username:
        return redirect("/friends/?error=You cannot invite yourself", status=401)

    try:
        friend: User = await User.objects.aget(username=username)
    except:
        return redirect("/friends/?error=No user found with this username", status=401)

    if getFriendship(user, friend) is None:
        return redirect("/friends/?error=This user is not your friend", status=401)

    if not userIsLoggedIn(friend):
        return redirect(f"/friends/?error={friend.username} is not online", status=401)

    message = json.dumps({
        "message": f"<a href=/pong/lobby/?opponent={user.username}>{user.username} invites you to play pong</a>",
        "refresh": ["/pong/"]
    })
    await sendMessageWS(friend, "notifications", message)
    return render(req, "pong/lobby.html", context={"opponent": friend})