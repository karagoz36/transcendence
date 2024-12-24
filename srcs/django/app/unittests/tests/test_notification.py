import json
from channels.testing import WebsocketCommunicator
from rest_framework.test import APITestCase, APIClient
from transcendence.asgi import application
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
        response = self.client.post("/api/friend/add", follow=True, data={"username": self.testUser.username})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.testUser.username in str(response.content))

        response = self.testClient.post("/api/friend/accept", follow=True, data={"friendID": self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.username in str(response.content))

    async def setUp(self):
        self.user: User = User.objects.create_user(username="ketrevis", password="ketrevis")
        self.testUser: User = User.objects.create_user(username="test", password="test")

        self.client = self.login(self.user.username, self.user.username)
        self.testClient = self.login(self.testUser.username, self.testUser.username)
    
        self.clientSocket = WebsocketCommunicator(application, "/websocket/notifications/")
        self.clientSocket.scope["user"] = self.user
        connected, _ = await self.clientSocket.connect()
        print(connected)
        self.addFriend()