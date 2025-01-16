from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.tournament import getTournaments

@login_required(login_url="/api/logout")
def response(request: Request) -> Response:
	user: User = request.user
	if user.is_anonymous:
		return redirect("/api/logout")

	tournaments = getTournaments(user)
	return render(request, "index.html",
		{"USERNAME": user.username, "tournaments": tournaments})