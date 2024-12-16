from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import cache

def userIsLoggedIn(user: User) -> bool:
	return cache.get(f"{user.id}_notifications") is not None

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
			await self.close()
			return
		cache.set(self.group_name, "")
		await self.channel_layer.group_add(self.group_name, self.channel_name)

	async def disconnect(self, close_code):
		print(f"WebSocket: {self.group_name} closed", flush=True)
		cache.delete(self.group_name)

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

class Messages(BaseConsumer):
	def __init__(self):
		super().__init__("messages")