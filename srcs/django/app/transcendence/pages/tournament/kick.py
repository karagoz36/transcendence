from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .create import tournaments, Tournament

@login_required(login_url="/api/logout")
async def response(request: Request) -> HttpResponse:
    user: User = request.user
    tournament = tournaments.get(user.id)
    id = request.query_params.get("id")

    if tournament is None:
        return redirect("/")
    if id is None:
        return redirect("/tournament/create")
    id = int(id)
    toKick: User = await User.objects.aget(id=id)
    await tournament.removePlayer(toKick)
    return redirect("/tournament/create")