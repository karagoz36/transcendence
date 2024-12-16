# chat/routing.py
from django.urls import re_path

from . import consumers

# DO NOT APPEND OR PREPEND SLASHES TO ROUTE
# ALWAYS START ROUTE WITH websocket/
websocket_urlpatterns = [
    re_path(r"websocket/notifications/", consumers.Notification.as_asgi()),
    re_path(r"websocket/messages/", consumers.Messages.as_asgi()),
]