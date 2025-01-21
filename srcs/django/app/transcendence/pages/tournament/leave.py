import json
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .create import tournaments
from utils.websocket import sendMessageWS

@login_required(login_url="/api/logout")
async def response(request: Request) -> Response:
    user: User = request.user
    id = request.query_params.get("id")

    if id is None:
        return redirect("/")

    id = int(id)
    tournament = tournaments.get(id)

    if tournament is None:
        return redirect("/")

    await tournament.removePlayer(user)
    msg = {"message": f"{user.username} left the tournament", "refresh": ["/", "/tournament/create/", "/tournament/lobby/"]}
    msg = json.dumps(msg)

    for player in tournament.players.values():
        await sendMessageWS(player, "notifications", msg)
    return redirect("/")