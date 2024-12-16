import json
from django.http.response import HttpResponse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from database.models import Messages, FriendList, getFriendship
from http.cookies import SimpleCookie

def testGetFriendship(user: User, friend: User) -> FriendList|None:
	friendship: FriendList
	try:
		friendship = FriendList.objects.get(user=user, friend=friend)
		return friendship
	except:
		pass
	try:
		friendship = FriendList.objects.get(user=friend, friend=user)
		return friendship
	except:
		pass
	return None

class FriendTest(APITestCase):
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
        testClient = self.login(self.testUser.username, self.testUser.username)

        response = self.client.post("/api/friend/add", follow=True, data={"username": self.testUser.username})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.testUser.username in str(response.content))

        response = testClient.post("/api/friend/accept", follow=True, data={"friendID": self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.username in str(response.content))

    def setUp(self):
        self.user: User = User.objects.create_user(username="ketrevis", password="ketrevis")
        self.testUser: User = User.objects.create_user(username="test", password="test")

        self.client = self.login(self.user.username, self.user.username)
        self.addFriend()
    
    def testsendMessage(self):
        str = "coucou ca va?"
        response = self.client.post("/api/friend/send-message", follow=True, data={"friendID": self.testUser.id, "message": str})
        self.assertEqual(response.status_code, 200)
    
        friendship = testGetFriendship(self.user, self.testUser)
        self.assertNotEqual(friendship, None)
    
        message: Messages = None
        try:
            message = Messages.objects.get(message=str)
        except:
            pass
        self.assertNotEqual(message, None)
    
        message: Messages = None
        try:
            message = Messages.objects.get(friendship=friendship)
        except:
            pass
        self.assertNotEqual(message, None)

        message: Messages = None
        try:
            message = Messages.objects.get(sender=self.user)
        except:
            pass
        self.assertNotEqual(message, None)

        message: Messages = None
        try:
            message = Messages.objects.get(message=str, friendship=friendship, sender=self.user)
        except:
            pass
        self.assertNotEqual(message, None)
