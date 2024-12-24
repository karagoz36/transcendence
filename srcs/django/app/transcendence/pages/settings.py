from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from database.models import UserProfile
from django.http import JsonResponse
import json

@login_required
def response(request):
    user = request.user

    profile, _ = UserProfile.objects.get_or_create(user=user)

    return render(request, "settings.html", {
        "user": user,
        "profile": profile,
        "message": None,
    })


# def handle_update_settings(request):
#     user = request.user
#     if not user.is_authenticated:
#         return JsonResponse({"error": "User not authenticated"}, status=401)

#     if request.method != 'POST':
#         return JsonResponse({"error": "Invalid HTTP method"}, status=405)

#     email = request.data.get('email')
#     is_2fa_enabled = request.data.get('is_2fa_enabled') == 'on'

#     if email:
#         user.email = email
#         user.save()

#     profile, _ = UserProfile.objects.get_or_create(user=user)
#     profile.is_2fa_enabled = is_2fa_enabled

#     if is_2fa_enabled and not profile.otp_secret:
#         profile.generate_otp_secret()

#     profile.save()

#     return JsonResponse({"message": "Settings updated successfully"}, status=200)

@login_required
def handle_update_settings(request):
    print("userreerer:")
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    try:
        # Charger les données JSON depuis la requête
        data = json.loads(request.body)
        email = data.get("email")
        is_2fa_enabled = data.get("is_2fa_enabled", False)

        # Validation des données
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        # Mettre à jour les données utilisateur
        user = request.user
        user.email = email
        user.save()

        # Mettre à jour le profil utilisateur
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.is_2fa_enabled = is_2fa_enabled
        profile.save()

        return JsonResponse({"message": "Settings updated successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
