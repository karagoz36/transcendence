from django.contrib.auth.models import User
from rest_framework.request import Request
from database.models import getFriendship
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from websockets.consumers import sendNotification

@login_required(login_url="/auth")
async def response(request: Request):
    friend: User
    user: User = request.user

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
    sendNotification(friend, {"message": f"{user.username} accepted your friend invitation.", "refresh": "/friends/"})
    return redirect("/friends?success=Friend invite accepted!")