from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

def response(request: Request) -> HttpResponse:
	return redirect("/auth?logout")