from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.tournament import getTournaments
from database.models import TournamentResults
from django.db.models import Sum

@login_required(login_url="/api/logout")
def response(request: Request) -> Response:
	user: User = request.user
	if user.is_anonymous:
		return redirect("/api/logout")

	tournament_results = TournamentResults.objects.values('player') \
        .annotate(total_score=Sum('score')) \
        .order_by('-total_score')
	tournament_results = TournamentResults.objects.select_related('player') \
        .values('player__id', 'player__username') \
        .annotate(total_score=Sum('score')) \
        .order_by('-total_score')
            
	tournaments = getTournaments(user)
 
	return render(request, "index.html",
		{"tournaments": tournaments,
     	"results": tournament_results,
      })