from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.tournament import getTournaments

@login_required(login_url="/api/logout")
def response(request: Request) -> HttpResponse:
	user: User = request.user
	if user.is_anonymous:
		return redirect("/api/logout")
	return render(request, "index.html",
		{"USERNAME": user.username, "tournaments": getTournaments(user)})