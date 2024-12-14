import json
from django.http.response import HttpResponse
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

        self.client = self.login(self.user.username, self.user.username)

    def testFriendListGET(self):
        response = self.client.get("/friends", follow=True)
        self.assertEqual(response.status_code, 201)

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
    
    def testAddSameUserTwice(self):
        self.sendFriendInvite(self.client, self.testUser.username, 200)
        self.sendFriendInvite(self.client, self.testUser.username, 401)
    
    def testAddYourself(self):
        response = self.client.post("/api/friend/add", follow=True, data={"username": self.user.username}) # trying to add yourself
        self.assertEqual(response.status_code, 401)

    def testAddBothWays(self):
        response: HttpResponse = self.client.get("/friends", follow=True)
    
        self.assertFalse(self.testUser.username in str(response.content))
        self.sendFriendInvite(self.client, self.testUser.username, 200)
    
        testClient = self.login(self.testUser.username, self.testUser.username)
        response = testClient.post("/api/friend/add", follow=True, data={"username": self.user.username})
        self.assertEqual(response.status_code, 401)
    
    def testRemoveUser(self):
        testClient = self.login(self.testUser.username, self.testUser.username)

        response = self.client.post("/api/friend/add", follow=True, data={"username": self.testUser.username})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.testUser.username in str(response.content))

        response = testClient.post("/api/friend/remove", follow=True, data={"friendID": self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.username not in str(response.content))

        response = testClient.post("/api/friend/remove", follow=True, data={"friendID": self.user.id})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/remove", follow=True, data={"friendID": self.testUser.id})
        self.assertEqual(response.status_code, 401)

    def testAcceptUser(self):
        testClient = self.login(self.testUser.username, self.testUser.username)

        response = self.client.post("/api/friend/add", follow=True, data={"username": self.testUser.username})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.testUser.username in str(response.content))

        response = testClient.post("/api/friend/accept", follow=True, data={"friendID": self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.username in str(response.content))
    
    def testInvalidData(self):
        response = self.client.post("/api/friend/add", follow=True, data={"username": "asdfklajsf"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/add", follow=True, data={"username": 10})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/remove", follow=True, data={"friendID": "asdfklajsf"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/remove", follow=True, data={"friendID": 11230981})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/accept", follow=True, data={"friendID": "asdfklajsf"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/accept", follow=True, data={"friendID": 11230981})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/api/friend/add", follow=True, data={})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/add", follow=True, data={})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/remove", follow=True, data={})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/remove", follow=True, data={})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/accept", follow=True, data={})
        self.assertEqual(response.status_code, 401)

        response = self.client.post("/api/friend/accept", follow=True, data={})
        self.assertEqual(response.status_code, 401)
    
    def testGet(self):
        response = self.client.get("/api/friend/accept")
        self.assertEqual(response.status_code, 405)

        response = self.client.get("/api/friend/add")
        self.assertEqual(response.status_code, 405)

        response = self.client.get("/api/friend/remove")
        self.assertEqual(response.status_code, 405)
