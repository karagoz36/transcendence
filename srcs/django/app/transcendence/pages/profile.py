from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models import PongHistory

async def getPongHistory(user: User):
    history = []
    res = PongHistory.objects.select_related("player2").filter(player1=user)

    async for game in res:
        history.append({
            "user": user,
            "opponent": game.player2,
            "user_score": game.player1_score,
            "opponent_score": game.player2_score
        })
    res = PongHistory.objects.select_related("player1").filter(player2=user)

    async for game in res:
        history.append({
            "user": user,
            "opponent": game.player1,
            "user_score": game.player2_score,
            "opponent_score": game.player1_score
        })
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
    await getPongHistory(user)
    return render(request, "profile/profile.html", context={"history": await getPongHistory(user)})