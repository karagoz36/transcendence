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

        profile, _ = UserProfile.objects.get_or_create(user=user)

        username = request.POST.get("username")
        email = request.POST.get("email")
        is_2fa_enabled = request.POST.get("is_2fa_enabled") == 'on'

        # # Gestion de l'avatar
        # avatar = request.FILES.get("avatar")
        # if avatar:
        #     if profile.avatar:
        #         # Supprimez l'ancien avatar s'il existe
        #         profile.avatar.delete(save=False)
        #     profile.avatar = avatar

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        # Enregistrez le profil mis à jour
        profile.save()


        # Mise à jour des autres champs
        if not username:
            return JsonResponse({"error": "Username is required"}, status=400)
        if len(username) < 3:
            return JsonResponse({"error": "Username must be at least 3 characters long"}, status=400)
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"error": "Wrong Email format"}, status=400)

        user.username = username
        user.email = email
        user.save()

        profile.is_2fa_enabled = is_2fa_enabled
        profile.save()

        return JsonResponse({"message": "Settings updated successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# @permission_classes([AllowAny])
# def handle_update_settings(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid HTTP method"}, status=405)

#     try:
#         data = json.loads(request.body)
#         username = data.get("username")
#         email = data.get("email")
#         is_2fa_enabled = data.get("is_2fa_enabled", False)

#         if not username:
#             return JsonResponse({"error": "Username is required"}, status=400)
        
#         # revoir les exigences du username
#         if len(username) < 3:
#             return JsonResponse({"error": "Username must be at least 3 characters long"}, status=400)
        
#         user = request.user
#         if user.is_anonymous:
#             return JsonResponse({"error": "Authentication required"}, status=401)
        
#         # Vérification de l'unicité du username
#         if User.objects.filter(username=username).exclude(id=user.id).exists():
#             return JsonResponse({"error": "Username already taken"}, status=400)


#         if not email:
#             return JsonResponse({"error": "Email is required"}, status=400)

#         try:
#             validate_email(email)
#         except ValidationError:
#             return JsonResponse({"error": "Wrong Email format"}, status=400)


#         user.username = username
#         user.email = email
#         user.save()

#         profile, _ = UserProfile.objects.get_or_create(user=user)
#         profile.is_2fa_enabled = is_2fa_enabled
#         profile.save()

#         return JsonResponse({"message": "Settings updated successfully"}, status=200)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
