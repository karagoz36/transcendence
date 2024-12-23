from rest_framework.request import Request
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from websockets.consumers import sendMessageWS
import json

@login_required(login_url="/api/logout")
async def response(req: Request):
    username = req.query_params.get("username")
    if username is None:
        return redirect("/play/?error=Invalid body", status=401)
    
    user: User = req.user
    if username == user.username:
        return redirect("/play/?error=You cannot invite yourself", status=401)
    friend: User = await User.objects.aget(username=username)
    message = json.dumps({"message": f"<a href=/play/>{user.username} invites you to play.</a>"})
    await sendMessageWS(friend, "notifications", message)
    return redirect(f"/play/?success=Game invitation sent to {username}")