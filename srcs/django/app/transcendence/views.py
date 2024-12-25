from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from adrf.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from django.core.cache import cache
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import pages

@api_view(['GET'])
async def auth(request: Request):
	return await pages.auth.response(request)

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
def register(request: Request):
	return pages.register.response(request)

@api_view(['GET'])
def index(request: Request):
	return pages.index.response(request)

@api_view(['GET'])
def settings(request: Request):
	return pages.settings.response(request)

@api_view(['GET'])
async def friends(request: Request):
	return await pages.friends.response(request)

@api_view(['GET'])
async def lobby(request: Request):
	return await pages.lobby.response(request)

@api_view(['POST'])
async def addFriend(request: Request):
	return await pages.addFriend.response(request)

@api_view(['POST'])
async def acceptFriend(request: Request):
	return await pages.acceptFriend.response(request)

@api_view(['POST'])
async def removeFriend(request: Request):
	return await pages.removeFriend.response(request)

@api_view(['POST'])
async def sendMessage(request: Request):
	return await pages.sendMessage.response(request)

@authentication_classes([])
@permission_classes([AllowAny])
def getToken(request: Request):
	view = TokenObtainPairView.as_view()
	return view(request)

@authentication_classes([])
@permission_classes([AllowAny])
def refreshToken(request: Request):
	view = TokenRefreshView.as_view()
	return view(request)