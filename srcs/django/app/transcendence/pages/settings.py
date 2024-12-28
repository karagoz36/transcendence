from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
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

@permission_classes([AllowAny])
def handle_update_settings(request):
    print("handle_update_settings called")
    if request.method != "POST":
        print("Invalid HTTP method")
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    try:
        print("Request body:", request.body)
        data = json.loads(request.body)
        email = data.get("email")
        is_2fa_enabled = data.get("is_2fa_enabled", False)

        if not email:
            print("Email is missing")
            return JsonResponse({"error": "Email is required"}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            print("Invalid email format")
            return JsonResponse({"error": "Wrong Email format"}, status=400)

        user = request.user
        print("User:", user)
        # if user.is_anonymous:
        #     print("User is anonymous")
        #     return JsonResponse({"error": "Authentication required"}, status=401)

        user.email = email
        user.save()
        print("Email updated:", user.email)

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.is_2fa_enabled = is_2fa_enabled
        profile.save()
        print("Profile updated:", profile)

        return JsonResponse({"message": "Settings updated successfully"}, status=200)
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"error": str(e)}, status=500)


# @permission_classes([AllowAny])
# def handle_update_settings(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid HTTP method"}, status=405)

#     try:
#         data = json.loads(request.body)
#         email = data.get("email")
#         is_2fa_enabled = data.get("is_2fa_enabled", False)

#         if not email:
#             return JsonResponse({"error": "Email is required"}, status=400)
#         try:
#             validate_email(email)
#         except ValidationError:
#             return JsonResponse({"error": "Wrong Email format"}, status=400)
#         user = request.user
#         user.email = email
#         user.save()

#         profile, _ = UserProfile.objects.get_or_create(user=user)
#         profile.is_2fa_enabled = is_2fa_enabled
#         profile.save()

#         return JsonResponse({"message": "Settings updated successfully"}, status=200)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
