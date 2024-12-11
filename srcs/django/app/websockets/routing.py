# chat/routing.py
from django.urls import re_path

from . import consumers

# DO NOT APPEND OR PREPEND SLASHES TO ROUTE
# ALWAYS START ROUTE WITH websocket/
websocket_urlpatterns = [
    re_path("websocket/notifications", consumers.Notification.as_asgi()),
]