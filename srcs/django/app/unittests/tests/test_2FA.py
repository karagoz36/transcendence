import os
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from database.models import UserProfile
from unittest.mock import patch
import json
import pyotp

class DoubleAuthTest(APITestCase):
    def login(self, username: str, password: str) -> APIClient:
        client = APIClient()
        response = client.post("/api/token", data={"username": username, "password": password})
        self.assertEqual(response.status_code, 200)
        cookies = json.loads(response.content)

        response = client.post("/api/login", data={"username": username, "password": password})
        self.assertEqual(response.status_code, 200)

        client.cookies['access_token'] = cookies['access']
        return client

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='sikaperski', password="Qwertyuiop12", email="user@example.fr")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            is_2fa_enabled=True,
            otp_secret=pyotp.random_base32()
        )
        self.client = self.login(username=self.user.username, password="Qwertyuiop12")

    @patch('transcendence.pages.auth.sendingEmail.delay')
    def test2faEmailSend(self, mock_send_mail):
        self.client.login(username='sikaperski', password="Qwertyuiop12")
        otp = pyotp.TOTP(self.user_profile.otp_secret).now()
        response = self.client.post('/api/login', {'username': 'sikaperski', 'password': 'Qwertyuiop12'}, format='json')
        self.assertTrue(mock_send_mail.called)
        mock_send_mail.assert_called_with(otp, self.user.email)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"is_2fa_enabled": True})

    def test2faValidOtp(self):
        otp = pyotp.TOTP(self.user_profile.otp_secret).now()
        response = self.client.post(
            "/api/verify_otp/",
            data={"username": "sikaperski", "otp": otp},
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "OTP verified successfully"})