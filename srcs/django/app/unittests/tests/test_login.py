import os
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class LoginTest(APITestCase):
	def setUp(self):
		self.client = APIClient()
		User.objects.create_user(username="ketrevis", password="ketrevis")

	def testGET(self):
		response = self.client.get("/api/login")
		self.assertEqual(response.status_code, 405) # forbidden method

	def testPOST(self):
		data = {"username": "ketrevis",  "password": "ketrevis"}
		response = self.client.post("/api/login", follow=True,
			data=data)
		self.assertEqual(response.status_code, 200)

	def testEmptyUsername(self):
		data = {"username": "",  "password": "ketrevis"}
		response = self.client.post("/api/login", follow=True,
			data=data)
		self.assertEqual(response.status_code, 401)

	def testEmptyPassword(self):
		data = {"username": "ketrevis",  "password": ""}
		response = self.client.post("/api/login", follow=True,
			data=data)
		self.assertEqual(response.status_code, 401)

	def testBothEmpty(self):
		data = {"username": "",  "password": ""}
		response = self.client.post("/api/login", follow=True,
			data=data)
		self.assertEqual(response.status_code, 401)

	def testInvalidUsername(self):
		data = {"username": "asldkfja",  "password": "ketrevis"}
		response = self.client.post("/api/login", follow=True,
			data=data)
		self.assertEqual(response.status_code, 401)

	def testInvalidPassword(self):
		data = {"username": "ketrevis",  "password": "sakdfhsa"}
		response = self.client.post("/api/login", follow=True,
			data=data)
		self.assertEqual(response.status_code, 401)