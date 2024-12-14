import os
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class RegisterTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def testGET(self):
        response = self.client.get("/api/register")
        self.assertEqual(response.status_code, 405) # forbidden method

    def testValidLogs(self):
        data = {"username": "ketrevis",  "password": "coucoucava"}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 200)

        data = {"username": "ketrevis",  "password": "coucoucava"}
        response = self.client.post("/api/login", follow=True,
            data=data)
        self.assertEqual(response.status_code, 200)

    def testEmptyUsername(self):
        data = {"username": "",  "password": "ketrevis"}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 401)

    def testEmptyPassword(self):
        data = {"username": "ketrevis",  "password": ""}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 401)
    
    def testBothEmpty(self):
        data = {"username": "",  "password": ""}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 401)
  
    def testPasswordTooShort(self):
        data = {"username": "ketrevis",  "password": "co"}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 401)
  
    def testUsernameTooShort(self):
        data = {"username": "co",  "password": "ketrevis"}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 401)
  
    def testBothTooShort(self):
        data = {"username": "co",  "password": "co"}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 401)

    def testSameUsernameAndPassword(self):
        data = {"username": "coucoucava",  "password": "coucoucava"}
        response = self.client.post("/api/register", follow=True,
            data=data)
        self.assertEqual(response.status_code, 401)