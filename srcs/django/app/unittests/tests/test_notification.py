import json
from channels.testing import WebsocketCommunicator
from rest_framework.test import APIClient, APITestCase
from websockets.consumers import Notification
from django.contrib.auth.models import User

class NotificationTest(APITestCase):
    def login(self, username: str, password: str) -> APIClient:
        client = APIClient()
        response = client.post("/api/token", data={"username": username, "password": password})
        self.assertEqual(response.status_code, 200) 
        cookies = json.loads(response.content)
        response = client.post("/api/login", data={"username": username, "password": password}, follow=True)
        self.assertEqual(response.status_code, 200)
        client.cookies['access_token'] = cookies['access']
        return client

    def addFriend(self):
        response = self.user["api"].post("/api/friend/add", follow=True, data={"username": self.test["user"]})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.test["user"].username in str(response.content))

        response = self.test["api"].post("/api/friend/accept", follow=True, data={"friendID": self.user["user"].id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user["user"].username in str(response.content))

    def setUp(self):
        self.user = {}
        User.objects.create_user(username="user", password="user")
        self.user["user"] = User.objects.get(username="user")
        self.user["api"] = self.login("user", "user")

        self.test = {}    
        User.objects.create_user(username="test", password="test")
        self.test["user"] = User.objects.get(username="test")
        self.test["api"] = self.login("test", "test")
        self.addFriend()

    async def connectWebSocket(self, user: User) -> WebsocketCommunicator:
        websocket = WebsocketCommunicator(Notification.as_asgi(), "websocket/notifications/")
        websocket.scope["user"] = user
        connected, _ = await websocket.connect()
        self.assertTrue(connected)
        return websocket

    async def testWithoutUser(self):
        websocket = WebsocketCommunicator(Notification.as_asgi(), "websocket/notifications/")
        connected, _ = await websocket.connect()
        self.assertTrue(connected)
        msg = await websocket.receive_output(timeout=5)
        self.assertEqual(msg.get("type"), "websocket.close")

    async def testBasicNotif(self):
        websockets = {
            "user": await self.connectWebSocket(self.user["user"]),
            "test": await self.connectWebSocket(self.test["user"])
        }
        message = await websockets["user"].receive_json_from()
        self.assertEqual(message["message"], "test logged in.")