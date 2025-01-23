from rest_framework.request import Request
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from adrf.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from django.core.cache import cache
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import pages
import pyotp
from django.http import JsonResponse
from django.middleware.csrf import get_token
from database.models import UserProfile

@api_view(['GET'])
async def auth(request: Request):
    return await pages.auth.response(request)

@api_view(['GET'])
async def auth_with_42(request: Request):
    return await pages.auth.response42(request)

@api_view(['GET'])
def callback_from_42(request: Request):
    return pages.auth.callback_from_42(request)

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

@api_view(['POST'])
def update_settings(request: Request):
    return pages.settings.handle_update_settings(request)

@api_view(['POST'])
def remove_avatar(request: Request):
    return pages.settings.handle_remove_avatar(request)

@api_view(['GET'])
async def friends(request: Request):
    return await pages.friends.response(request)

@api_view(['GET'])
async def lobby(request: Request):
    return await pages.lobby.response(request)

@api_view(['GET'])
def play(request: Request):
    return pages.play.response(request)

@api_view(['GET'])
async def profile(request: Request):
    return await pages.profile.response(request)

@api_view(['GET'])
def profile_list(request: Request):
    return pages.profile_list.response(request)

# @api_view(['GET'])
# def profile_detail(request: Request, id):
#     return pages.profile_detail.response(request, id)

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
@permission_classes([AllowAny])
def is_2fa_enabled(request):
    username = request.data.get("username")
    if not username:
        return Response({"error": "Username is required"}, status=400)
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        return Response({"is_2fa_enabled": user_profile.is_2fa_enabled}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except UserProfile.DoesNotExist:
        return Response({"is_2fa_enabled": False}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    username = request.data.get("username")
    otp = request.data.get("otp")
    if not username or not otp:
        return Response({"error": "Missing username or OTP"}, status=400)
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        totp = pyotp.TOTP(user_profile.otp_secret)
        if totp.verify(otp, valid_window=2):
            return Response({"message": "OTP verified successfully"}, status=200)
        else:
            return Response({"error": "Invalid OTP"}, status=400)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found"}, status=404)

@api_view(['POST'])
async def sendMessage(request: Request):
    print(request.user)
    return await pages.sendMessage.response(request)

@api_view(['POST'])
async def openMessage(request: Request):
    return await pages.openMessage.response(request)

@authentication_classes([])
@permission_classes([AllowAny])
def getToken(request: Request):
    view = TokenObtainPairView.as_view()
    return view(request)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

@authentication_classes([])
@permission_classes([AllowAny])
def refreshToken(request: Request):
    view = TokenRefreshView.as_view()
    return view(request)