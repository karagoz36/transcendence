from channels.generic.websocket import AsyncWebsocketConsumer

class Notification(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()
        self.send("test")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data: str):
        self.send(text_data=text_data)