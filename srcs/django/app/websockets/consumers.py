from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User
import json
from transcendence.pages.friends import getFriends

onlineUsers = {}

def userIsLoggedIn(user: User) -> bool:
	return onlineUsers.get(user.id) is not None

async def sendMessageWS(receiver: User, groupName: str, message: str) -> None:
	layer: BaseChannelLayer = get_channel_layer()
	await layer.group_send(f"{receiver.id}_{groupName}", {
		"type": "sendMessage",
		"message": message
	})

class BaseConsumer(AsyncWebsocketConsumer):
	def __init__(self, consumerName: str):
		super().__init__()
		self.consumerName = consumerName

	async def connect(self):
		user: User = self.scope["user"]
		await self.accept()
		self.group_name = f"{user.id}_{self.consumerName}"
		if user.username == "":
			await self.close(code=4000)
			return
		print(f"WebSocket: {self.group_name} connected", flush=True)
		onlineUsers[user.id] = True
		await self.channel_layer.group_add(self.group_name, self.channel_name)

	async def disconnect(self, close_code):
		user: User = self.scope["user"]
		print(f"WebSocket: {self.group_name} disconnected", flush=True)
		if user.id in onlineUsers:
			del onlineUsers[user.id]

	async def receive(self, text_data: str):
		pass
	
	async def sendMessage(self, event):
		message: str = event["message"]
		await self.send(message)
	
	async def closeConnection(self, event):
		await self.close()

class Notification(BaseConsumer):
	def __init__(self):
		super().__init__("notifications")
	
	async def connect(self):
		await super().connect()
		user: User = self.scope["user"]
		if user.username == "":
			return

		friends = await getFriends(user)
		for friend in friends:
			receiver: User = await User.objects.aget(id=friend["id"])
			message = json.dumps({
				"message": f"{user.username} just logged in.",
				"refresh": ["/friends/", "/play/"]
			})
			await sendMessageWS(receiver, "notifications", message)

	async def disconnect(self, close_code):
		await super().disconnect(close_code)

		user: User = self.scope["user"]
		if user.username == "":
			return

		friends = await getFriends(user)
		for friend in friends:
			receiver: User = await User.objects.aget(id=friend["id"])
			message = json.dumps({"message": f"{user.username} just logged out."})
			await sendMessageWS(receiver, "notifications", message)

class Messages(BaseConsumer):
	def __init__(self):
		super().__init__("messages")