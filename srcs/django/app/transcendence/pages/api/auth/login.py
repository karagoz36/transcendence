from django.shortcuts import redirect
from rest_framework.request import Request
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login
from database.models import UserProfile
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from django.core.mail import send_mail
from transcendence.pages.auth import sendingEmail
import pyotp

@authentication_classes([])
@permission_classes([AllowAny])
def response(request: Request) -> JsonResponse:
    if "username" not in request.data or "password" not in request.data:
        return JsonResponse({"error": "Missing password or username"}, status=400)

    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    try:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.is_2fa_enabled:
            if not user_profile.otp_secret:
                user_profile.generate_otp_secret()
            otp = pyotp.TOTP(user_profile.otp_secret).now()
            sendingEmail.delay(otp, user.email)
            login(request, user)
            return JsonResponse({"is_2fa_enabled": True}, status=200)
    except UserProfile.DoesNotExist:
        pass
    login(request, user)
    return JsonResponse({"is_2fa_enabled": False}, status=200)