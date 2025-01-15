from django.contrib.auth.models import User
from database.models import FriendList
from .users import userIsLoggedIn

class FriendData:
    id: int
    username: str
    status: str

def userToDict(user: User) -> FriendData:
    data = FriendData()
    data.id = user.id
    data.username = user.username
    data.status = "online" if userIsLoggedIn(user) else "offline"
    return data

async def getFriends(user: User) -> list[FriendData]:
    res = []

    friends = FriendList.objects.select_related("friend").filter(user=user, invitePending=False)
    async for friend in friends:
        res.append(userToDict(friend.friend))

    friends = FriendList.objects.select_related("user").filter(friend=user, invitePending=False)
    async for friend in friends:
        res.append(userToDict(friend.user))
    return res