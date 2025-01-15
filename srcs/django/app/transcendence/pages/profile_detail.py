from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models import UserProfile
from django.shortcuts import get_object_or_404
from django.http import Http404

def response(request: Request, id):
    # allUsers = UserProfile.objects.all()

    # user = get_object_or_404(UserProfile, user_id=id)
    try:
        user = UserProfile.objects.get(user_id=id)
    except UserProfile.DoesNotExist:
        return redirect('index')
    context = {'user': user}
    return render(request,
        'profile/profile_detail.html',
        context)
