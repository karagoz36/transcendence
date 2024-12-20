from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from database.models import UserProfile

@login_required
def response(request):
    user = request.user
    message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        is_2fa_enabled = request.POST.get('is_2fa_enabled') == 'on'

        user.email = email
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.is_2fa_enabled = is_2fa_enabled

        if is_2fa_enabled and not profile.otp_secret:
            profile.generate_otp_secret()

        profile.save()
        message = "Settings updated successfully!"

    profile, _ = UserProfile.objects.get_or_create(user=user)

    return render(request, "settings.html", {
        "user": user,
        "profile": profile,
        "message": message
    })