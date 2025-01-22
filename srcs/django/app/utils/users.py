import json
from django.contrib.auth.models import User
from .websocket import sendMessageWS

onlineUsers: dict[int, User] = {}

def userIsLoggedIn(user: User) -> bool:
	return onlineUsers.get(user.id) != None

async def notifEveryone(msg: dict, blacklist: list[User] = []):
	msg: str = json.dumps(msg)
	for user in onlineUsers.values():
		if user not in blacklist:
			await sendMessageWS(user, "notifications", msg)