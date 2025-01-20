from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models import PongHistory
from asgiref.sync import sync_to_async
from django.db.models import Q

@sync_to_async
def getStats(user: User):
    wins = PongHistory.objects.filter(winner=user).count()

    losses = PongHistory.objects.filter(
        Q(player1=user) | Q(player2=user)
    ).exclude(winner=user).count()

    return {
        "wins": wins,
        "losses": losses,
    }

@sync_to_async
def getPongHistory(user: User):
    history = []
    res = PongHistory.objects.select_related("player2").filter(player1=user)

    for game in res:
        history.append({
            "user": user,
            "opponent": game.player2,
            "user_score": game.player1_score,
            "opponent_score": game.player2_score,
            "game_date": game.game_date,
            "winner": game.winner
        })
    res = PongHistory.objects.select_related("player1").filter(player2=user)

    for game in res:
        history.append({
            "user": user,
            "opponent": game.player1,
            "user_score": game.player2_score,
            "opponent_score": game.player1_score,
            "game_date": game.game_date,
            "winner": game.winner
        })
    history.sort(key=lambda x: x["game_date"], reverse=True)
    return history

async def response(request: Request):

    id: int = request.query_params.get("id")
    user: User = None

    if id is None:
        return redirect("/")
    try:
        user = await User.objects.aget(id=id)
    except:
        return redirect("/")

    context = {'user': user,
              "history": await getPongHistory(user),
              "stats": await getStats(user) }
    return render(request, "profile/profile.html", context)
