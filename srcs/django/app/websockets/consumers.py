# chat/consumers.py
import json

from channels.generic.websocket import WebsocketConsumer


class Notification(WebsocketConsumer):
    connections: list = []
    def connect(self):
        self.connections.append(self)
        print(self.connections, flush=True)
        self.accept()
        self.send("test")

    def disconnect(self, close_code):
        self.connections.remove(self)

    def receive(self, text_data: str):
        self.send(text_data=text_data)