from django.contrib.auth.models import User

onlineUsers = {}

def userIsLoggedIn(user: User) -> bool:
	return onlineUsers.get(user.id) == True