from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User, AnonymousUser

async def sendNotification(receiver: User, message: str) -> None:
	layer: BaseChannelLayer = get_channel_layer()
	print(receiver.username, flush=True)
	print(message, flush=True)

	await layer.group_send(f"{receiver.username}_notifications", {
		"type": "sendMessage",
		"message": message
	})

class Notification(AsyncWebsocketConsumer):
	async def connect(self):
		user: User = self.scope["user"]
		await self.accept()
		if user.username == "":
			await self.send("Error: Not logged in")
			return
		self.group_name = f"{user.username}_notifications"
		await self.channel_layer.group_add(self.group_name, self.channel_name)

	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data: str):
		pass
	
	async def sendMessage(self, event):
		message: str = event["message"]
		await self.send(message)