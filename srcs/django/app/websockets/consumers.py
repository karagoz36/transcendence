from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User, AnonymousUser
import json

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
		await self.channel_layer.group_add(self.group_name, self.channel_name)

	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data: str):
		pass
	
	async def sendMessage(self, event):
		message: str = event["message"]
		await self.send(message)
	
	async def closeConnection(self, event):
		await self.close()