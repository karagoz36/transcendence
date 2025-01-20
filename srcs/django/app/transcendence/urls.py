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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
    path("settings/", views.settings, name="settings"),
    path("friends/", views.friends, name="friends"),
    path("profile/", views.profile, name="profile"),
    path("profile_list/", views.profile_list, name="profile_list"),
    # path("profile/<int:id>/", views.profile_detail, name="profile_detail"),
    # path("prometheus/", views.prometheus, name="profile"),

    path("pong/lobby/", views.lobby, name="lobby"),
    path("pong/play/", views.play, name="play"),

    path("api/login", views.login, name="login"),
    path("api/logout", views.logout, name="logout"),
    path("api/register", views.register, name="register"),

    path("api/friend/add", views.addFriend, name="addFriend"),
    path("api/friend/accept", views.acceptFriend, name="acceptFriend"),
    path("api/friend/remove", views.removeFriend, name="rejectFriend"),
    path("api/friend/send-message", views.sendMessage, name="sendMessage"),

    path("api/token", views.getToken, name="createToken"),
    path("api/token/refresh", views.refreshToken, name="refreshToken"),
    path("api/settings/update/", views.update_settings, name="update_settings"),
    path("api/user/is_2fa_enabled/", views.is_2fa_enabled, name="is_2fa_enabled"),
    path("api/verify_otp/", views.verify_otp, name="verify_otp"),
    path("api/csrf-token/", views.get_csrf_token, name="get_csrf_token"),
    path('auth/login42/', views.auth_with_42, name='login42'),
    path('auth/callback42/', views.callback_from_42, name='callback42'),
]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

