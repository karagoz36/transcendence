from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .create import tournaments, Tournament
import asyncio

@login_required(login_url="/api/logout")
async def response(request: Request) -> Response:
    user: User = request.user
    tournament: Tournament = tournaments.get(user.id)

    if tournament is None:
        return redirect("/")
    await tournament.launchGame()
    await asyncio.sleep(10)
    return redirect("/")