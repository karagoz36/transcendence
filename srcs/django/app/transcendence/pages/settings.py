
from django.shortcuts import render
from database.models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required(login_url="/api/logout")
def response(request):
    user = request.user

    profile, _ = UserProfile.objects.get_or_create(user=user)

    return render(request, "settings.html", {
        "user": user,
        "profile": profile,
        "message": None,
    })
    