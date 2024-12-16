from django.db import models
from django.contrib.auth.models import User

class FriendList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendOf")
    invitePending = models.BooleanField(default=True)

async def getFriendship(user: User, friend: User) -> FriendList|None:
	friendship: FriendList
	try:
		friendship = await FriendList.objects.aget(user=user, friend=friend)
		return friendship
	except:
		pass
	try:
		friendship = await FriendList.objects.aget(user=friend, friend=user)
		return friendship
	except:
		pass
	return None

class Messages(models.Model):
	friendship = models.ForeignKey(FriendList, on_delete=models.CASCADE)
	message = models.TextField()
	sender = models.ForeignKey(User, on_delete=models.CASCADE)