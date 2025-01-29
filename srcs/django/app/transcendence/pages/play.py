from rest_framework.request import Request
from django.shortcuts import render

def response(request: Request):
    return render(request, "pong/play.html")