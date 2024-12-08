from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from transcendence import api

@api_view(['GET'])
def auth(request: Request):
    return api.auth.response(request)

@api_view(['POST'])
def login(request: Request):
    return api.login.response(request)

@api_view(['GET'])
def index(request: Request):
    return api.index.response(request)

@api_view(['GET'])
def logout(request: Request):
    print(request.method,flush=True)
    return api.logout.response(request)