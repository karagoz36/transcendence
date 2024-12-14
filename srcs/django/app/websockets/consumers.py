from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import cache

def userIsLoggedIn(user: User) -> bool:
	return cache.get(f"{user.id}_notifications") is not None

async def sendNotification(receiver: User, message: str) -> None:
	layer: BaseChannelLayer = get_channel_layer()

	await layer.group_send(f"{receiver.id}_notifications", {
		"type": "sendMessage",
		"message": message
	})

class Notification(AsyncWebsocketConsumer):
	async def connect(self):
		user: User = self.scope["user"]
		await self.accept()
		if user.username == "":
			await self.close()
			return
		self.group_name = f"{user.id}_notifications"
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