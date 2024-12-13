from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from adrf.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from . import pages

@api_view(['GET'])
def auth(request: Request):
    return pages.auth.response(request)

@api_view(['GET'])
def logout(request: Request):
    return pages.logout.response(request)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request: Request):
    return pages.login.response(request)
	
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
async def register(request: Request):
    return await pages.register.response(request)

@api_view(['GET'])
async def index(request: Request):
    return await pages.index.response(request)

@api_view(['GET'])
def settings(request: Request):
    return pages.settings.response(request)

@api_view(['GET'])
def friends(request: Request):
    return pages.friends.response(request)

@api_view(['POST'])
def addFriend(request: Request):
    return pages.addFriend.response(request)

@api_view(['POST'])
def acceptFriend(request: Request):
    return pages.acceptFriend.response(request)

@api_view(['POST'])
def rejectFriend(request: Request):
    return pages.rejectFriend.response(request)