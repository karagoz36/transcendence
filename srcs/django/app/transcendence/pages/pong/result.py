from rest_framework.request import Request
from django.shortcuts import render
from database.models import PongHistory

def response(request: Request):

    game_id: int = request.query_params.get("game")
    if not game_id:
        return redirect("/")
    game = PongHistory.objects.get(id=game_id)
    
    if game is None:
        return redirect("/")

    if game.player1_score > game.player2_score:
        winner = game.player1
    elif game.player2_score > game.player1_score:
        winner = game.player2
        
    is_winner = request.user == winner
    
    context = {'game': game,
        'is_winner': is_winner,
        'winner': winner,
        }
    
    return render(request, "pong/result.html", context)