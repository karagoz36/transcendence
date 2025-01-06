from django.contrib.auth.models import User
from database.models import FriendList
from .users import userIsLoggedIn

def userToDict(user: User) -> dict:
    return {
       "id": user.id,
        "username": user.username,
        "status": "online" if userIsLoggedIn(user) else "offline",
        }

async def getFriends(user: User):
    res = []

    friends = FriendList.objects.select_related("friend").filter(user=user, invitePending=False)
    async for friend in friends:
        res.append(userToDict(friend.friend))

    friends = FriendList.objects.select_related("user").filter(friend=user, invitePending=False)
    async for friend in friends:
        res.append(userToDict(friend.user))
    return res