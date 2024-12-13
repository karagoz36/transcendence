from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User, AnonymousUser

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
		message = event["message"]
		await self.send(message)