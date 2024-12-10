from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def response(request: Request) -> HttpResponse:
	friends = ["test", "oui", "coucou"]
	return render(request, "friends.html", {"friends": friends})