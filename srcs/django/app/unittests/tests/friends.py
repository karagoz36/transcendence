import json
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from http.cookies import SimpleCookie

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

    def setUp(self):
        self.user = User.objects.create_user(username="ketrevis", password="ketrevis")
        self.testUser = User.objects.create_user(username="test", password="test")

        self.client = self.login("ketrevis", "ketrevis")

    def testFriendListGET(self):
        response = self.client.get("/friends", follow=True)
        self.assertEqual(response.status_code, 200)

    def testAddEmptyFriend(self):
        response = self.client.post("/api/friend/add", follow=True)
        self.assertEqual(response.status_code, 401)

    def testAddNonExistingFriend(self):
        response = self.client.post("/api/friend/add", follow=True, data={"username": "asdflkaj"})
        self.assertEqual(response.status_code, 401)
    
    def sendFriendInvite(self, client: APIClient, username: str, expectedCode: int):
        response = client.post("/api/friend/add", follow=True, data={"username": username})
        self.assertEqual(response.status_code, expectedCode)

        response = client.get("/friends", follow=True)
        self.assertTrue(username in str(response.content))

    def testAddTestUser(self):
        response = self.client.get("/friends", follow=True)
        testUser = {"name": "test", "client": APIClient()}
    
        self.assertFalse(testUser["name"] in str(response.content))
        self.sendFriendInvite(self.client, testUser["name"], 200)
        self.sendFriendInvite(self.client, testUser["name"], 401)
        response = self.client.post("/api/friend/add", follow=True, data={"username": "ketrevis"})
        self.assertEqual(response.status_code, 401)
    
        testUser["client"] = self.login(testUser["name"], testUser["name"])
        self.sendFriendInvite(testUser["client"], "ketrevis", 401)
        response = self.client.post("/api/friend/add", follow=True, data={"username": testUser["name"]})
        self.assertEqual(response.status_code, 401)
        
        testUser["client"].post("/api/friend/accept", follow=True, data={""})