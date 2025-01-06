import json
from django.contrib.auth.models import User
from database.models import FriendList, getFriendship
from rest_framework.request import Request
from django.shortcuts import redirect
from websockets.consumers import sendMessageWS

async def response(request: Request):
	type = ""
	if "type" in request.query_params:
		type = request.query_params["type"]
	user: User = request.user
	friend: User

	if "friendID" not in request.data:
		return redirect("/friends?error=friendID must be present in body request", status=400)

	id: int = request.data["friendID"]
	try:
		friend = await User.objects.aget(id=id)
	except:
		return redirect("/friends?error=Invalid friendID sent", status=400)

	friendship: FriendList = await getFriendship(user, friend)
	if friendship is None:
		return redirect("/friends?error=Friendship not found", status=400)
	await friendship.adelete()
	if type == "remove":
		await sendMessageWS(friend, "notifications",
			json.dumps({"message": f"{user.username} removed you from your friend list.", "refresh": ["/friends/"]}))
	elif type == "reject":
		await sendMessageWS(friend, "notifications",
			json.dumps({"message": f"{user.username} rejected your friend invitation.", "refresh": ["/friends/"]}))
	return redirect("/friends?success=Friend successfully removed")