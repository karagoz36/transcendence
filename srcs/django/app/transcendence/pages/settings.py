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

@login_required
def handle_update_settings(request):
    print("userreerer:")
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        is_2fa_enabled = data.get("is_2fa_enabled", False)

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        user = request.user
        user.email = email
        user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.is_2fa_enabled = is_2fa_enabled
        profile.save()

        return JsonResponse({"message": "Settings updated successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
