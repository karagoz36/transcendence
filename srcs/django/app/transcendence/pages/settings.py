from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from django.shortcuts import render
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from database.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.files.storage import default_storage
from transcendence.pages.api.auth.register import usernamePolicy, passwordPolicy

@login_required(login_url="/api/logout")
def response(request):
    user = request.user

    profile, _ = UserProfile.objects.get_or_create(user=user)

    return render(request, "settings.html", {
        "user": user,
        "profile": profile,
        "message": None,
    })
    
@permission_classes([AllowAny])
def handle_update_settings(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    try:
        user = request.user
        if user.is_anonymous:
            return JsonResponse({"error": "Authentication required"}, status=401)
        
        # username = request.POST.get("username")
        alias = request.POST.get("alias")
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        # is_2fa_enabled = request.POST.get("is_2fa_enabled", False)
        is_2fa_enabled = request.POST.get("is_2fa_enabled", "false").lower() == "true"
        avatar = request.FILES.get("avatar")  # Récupère le fichier avatar

        # # verification du username
        # if not username:
        #     return JsonResponse({"error": "Username is required"}, status=400)
        # err: str = usernamePolicy(username)
        # if err != "":
        #     return JsonResponse({"error": "Username must be at least 5 characters long"}, status=400)
        
        # verification du password
        if password:
            err = passwordPolicy(password)
            if err != "":
                return JsonResponse({"error": "Password must be at least 8 characters long"}, status=400)

        if password == user.username:
            return JsonResponse({"error": "Username and password cannot be the same"}, status=400)

        profile, _ = UserProfile.objects.get_or_create(user=user)

        if avatar:
            profile.avatar = avatar

        if is_2fa_enabled:
            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({"error": "Wrong Email format"}, status=400)

        if UserProfile.objects.filter(alias=alias).exclude(id=user.id).exists():
            return JsonResponse({"error": "Alias already taken"}, status=400)

        # user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        profile.is_2fa_enabled = is_2fa_enabled
        profile.alias = alias
        profile.save()

        return JsonResponse({"message": "Settings updated successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@permission_classes([AllowAny])
def handle_remove_avatar(request):
    try:
        user = request.user
        if user.is_anonymous:
            return JsonResponse({"error": "Authentication required"}, status=401)
        profile, _ = UserProfile.objects.get_or_create(user=user)

        if profile.avatar:
            profile.avatar.delete(save=False)  # Supprimer le fichier
            profile.avatar = None  # Réinitialiser le champ
            profile.save()
        return JsonResponse({"message": "Avatar removed successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

