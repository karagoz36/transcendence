from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .create import tournaments, Tournament

@login_required(login_url="/api/logout")
async def response(request: Request) -> HttpResponse:
    user: User = request.user
    username = request.query_params.get("username")

    if username is None:
        return redirect("/tournament/create/")
    
    if username == user.username:
        return redirect("/tournament/create/?error=You cannot invite yourself to you tournament")
    try:
        invited: User = await User.objects.aget(username=username)
    except:
        return redirect("/tournament/create/?error=This user does not exist.")

    tournament = tournaments.get(user.id)
    if tournament is None:
        tournament = Tournament(user)
        tournaments[user.id] = tournament
    await tournament.inviteUser(invited)
    return redirect("/tournament/create/?success=Invite sent.")