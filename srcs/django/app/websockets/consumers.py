from channels.generic.websocket import WebsocketConsumer

class Notification(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send("test")

    def disconnect(self, close_code):
        pass

    def receive(self, text_data: str):
        self.send(text_data=text_data)