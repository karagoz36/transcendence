"""
URL configuration for transcendence project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
    path("settings/", views.settings, name="settings"),
    path("friends/", views.friends, name="friends"),
    path("api/login", views.login, name="login"),
    path("api/logout", views.logout, name="logout"),
    path("api/register", views.register, name="register"),
    path("api/friend/add", views.addFriend, name="addFriend"),
    path("api/friend/accept", views.acceptFriend, name="acceptFriend"),
    path("api/friend/reject", views.rejectFriend, name="rejectFriend"),
    path("api/token", views.rejectFriend, name="rejectFriend"),
    path("api/token/refresh", views.rejectFriend, name="rejectFriend"),
]