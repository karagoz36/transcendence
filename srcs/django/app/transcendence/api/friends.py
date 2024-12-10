from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def response(request: Request) -> HttpResponse:
	friends = [{"username": "test", "status": "online", "id": 0}]
	return render(request, "friendlist.html", {"friends": friends})