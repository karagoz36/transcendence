from django.db import models
from django.contrib.auth.models import User

class FriendList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendOf")
    invitePending = models.BooleanField(default=True)
