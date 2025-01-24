from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .create import tournaments

@login_required(login_url="/api/logout")
async def response(request: Request) -> Response:
    user: User = request.user
    id: int = request.query_params.get("id")

    if id is None:
        return redirect("/")
    id = int(id)
    tournament = tournaments.get(id)

    if id == user.id:
        return redirect("/")
    if tournament is None:
        return redirect("/")
    if tournament.started:
        return redirect("/")
    await tournament.addPlayer(user)
    return render(request, "tournament/lobby.html", context={
            "players": tournament.players.values(),
            "organizer": tournament.organizer
        })