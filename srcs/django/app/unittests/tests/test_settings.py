from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from database.models import UserProfile
import json


class SettingsTest(APITestCase):
    def login(self, username: str, password: str) -> APIClient:
        """Connecte un utilisateur et retourne un client API authentifié."""
        client = APIClient()
        response = client.post("/api/token", data={"username": username, "password": password})
        self.assertEqual(response.status_code, 200) 
        cookies = json.loads(response.content)

        response = client.post("/api/login", data={"username": username, "password": password}, follow=True)
        self.assertEqual(response.status_code, 200)

        client.cookies['access_token'] = cookies['access']
        return client

    def setUp(self):
        """Configuration initiale des tests."""
        self.user = User.objects.create_user(
            username='sikaperski',
            password='Qwertyuiop12',
            email='oldemail@example.com'
        )
        self.client = self.login(self.user.username, "Qwertyuiop12")

    def test_update_settings_invalid_method(self):
        """Test si une méthode non-POST retourne une erreur 405."""
        response = self.client.get('/api/settings/update/')
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'detail': 'Method "GET" not allowed.'})

    def test_update_settings_missing_email(self):
        """Test si l'email manquant retourne une erreur 400."""
        response = self.client.post(
            '/api/settings/update/',
            data=json.dumps({'is_2fa_enabled': True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Email is required'})

    def test_update_settings_invalid_email_format(self):
        """Test si un email avec un format incorrect retourne une erreur 400."""
        response = self.client.post(
            '/api/settings/update/',
            data=json.dumps({'email': 'invalid-email', 'is_2fa_enabled': True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Wrong Email format"})

    def test_update_settings_successful(self):
        """Test si la mise à jour des paramètres est réussie."""
        new_email = 'newemail@example.com'
        response = self.client.post(
            '/api/settings/update/',
            data=json.dumps({'email': new_email, 'is_2fa_enabled': True}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Settings updated successfully"})

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, new_email)

        profile = UserProfile.objects.get(user=self.user)
        self.assertTrue(profile.is_2fa_enabled)

    def test_update_settings_unauthenticated(self):
        """Test si un utilisateur non authentifié retourne une erreur 401."""
        unauth_client = APIClient()
        response = unauth_client.post(
            '/api/settings/update/',
            data=json.dumps({'email': 'unauth@example.com', 'is_2fa_enabled': True}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Authentication required'})
