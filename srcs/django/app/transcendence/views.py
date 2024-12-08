from django.http.request import HttpRequest
from django.contrib.auth.models import User
from transcendence import api

def index(request: HttpRequest):
    return api.index.response(request)

def login(request: HttpRequest):
    return api.login.response(request)