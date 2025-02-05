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
	format = "<a href='/friends' style='text-decoration: none;'>"
	if type == "remove":
		format += f"{user.username} removed you from your friend list."
		format += "</a>"
		dict = {"message": format, "refresh": ["/friends/"]}
		await sendMessageWS(friend, "notifications", json.dumps(dict))
	elif type == "reject":
		format += f"{user.username} rejected your friend invitation."
		format += "</a>"
		dict = {"message": format, "refresh": ["/friends/"]}
		await sendMessageWS(friend, "notifications", json.dumps(dict))
	return redirect("/friends?success=Friend successfully removed")