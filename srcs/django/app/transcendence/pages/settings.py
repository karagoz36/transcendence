from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from database.models import UserProfile

@login_required
def response(request: Request):
    if request.method == 'POST':
        # Update email
        email = request.POST.get('email')
        is_2fa_enabled = request.POST.get('is_2fa_enabled') == 'on'

        user = request.user
        user.email = email
        user.save()

        # Update 2FA status in the UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.is_2fa_enabled = is_2fa_enabled

        # Generate OTP secret if enabling 2FA for the first time
        if is_2fa_enabled and not profile.otp_secret:
            profile.generate_otp_secret()

        profile.save()

        # Provide feedback to the user
        return render(request, "settings.html", {"user": user, "message": "Settings updated successfully!"})

    # GET request - Render the settings page
    return render(request, "settings.html", {"user": request.user})
