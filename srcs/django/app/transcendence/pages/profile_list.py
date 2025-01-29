from rest_framework.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models import UserProfile

def response(request: Request):
   profiles = UserProfile.objects.all()
   return render(request,
           'profile/profile_list.html',  # pointe vers le nouveau nom de modèle
           {'profiles': profiles})
