from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from django.core.files.uploadedfile import UploadedFile
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from database.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from transcendence.pages.api.auth.register import usernamePolicy, passwordPolicy


def update_username(username: str, user: User):
    if not username:
        return {"message": "Username is required"}
    
    if User.objects.filter(username=username).exclude(id=user.id).exists():
        return {"message": "Username already taken"}

    err: str = usernamePolicy(username)
    if err != "":
        return {"message": "Username must be at least 5 characters long"}
    
    user.username = username
    user.save()
    
def update_email_2fa(email: str, is_2fa_enabled: bool, user: User, profile: UserProfile):
    if is_2fa_enabled:
        if not email:
            return {"message": "Email is required"}
    try:
        validate_email(email)
    except ValidationError:
        return {"message": "Wrong Email format"}
        
    user.email = email
    user.save()
    profile.is_2fa_enabled = is_2fa_enabled
    profile.save()
    
def update_password(password: str, user: User):
    err = passwordPolicy(password)
    if err != "":
        return {"message": "Password must be at least 8 characters long"}
        
    if password == user.username:
        return ({"message": "Username and password cannot be the same"})
    
    user.set_password(password)
    user.save()
    return None

def update_avatar(avatar: UploadedFile, profile: UserProfile):
    if avatar:
        profile.avatar = avatar
        profile.save()
    return None

    
@login_required(login_url="/api/logout")
@permission_classes([AllowAny])
def handle_update_settings(request: Request):
    if request.method != "POST":
        return JsonResponse({"message": "Invalid HTTP method"}, status=405)  
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
        
    username = request.POST.get("username")
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password")
    is_2fa_enabled = request.POST.get("is_2fa_enabled", "false").lower() == "true"
    avatar = request.FILES.get("avatar")
    
    message = None

    message = update_username(username, user)
    if not message and email or is_2fa_enabled:
        message = update_email_2fa(email, is_2fa_enabled, user, profile)
    if not message and password:
        message = update_password(password, user)
    if not message and avatar:
        message = update_avatar(avatar, profile)
        
    if message:
        return JsonResponse(message, status=400)
    
    return JsonResponse({"message": "Settings updated successfully"}, status=200)

@permission_classes([AllowAny])
def handle_remove_avatar(request):
    try:
        user = request.user
        if user.is_anonymous:
            return JsonResponse({"message": "Authentication required"}, status=401)
        profile, _ = UserProfile.objects.get_or_create(user=user)

        if profile.avatar:
            profile.avatar.delete(save=False)
            profile.avatar = None
            profile.save()
        return JsonResponse({"message": "Avatar removed successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

