from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User


class LoginSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass'
        )

    def test_valid_login(self):
        data = {'email': 'testuser@example.com', 'password': 'testpass'}
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_id', response.data)

    def test_invalid_email(self):
        data = {'email': 'invalid@example.com', 'password': 'testpass'}
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_invalid_password(self):
        data = {'email': 'testuser@example.com', 'password': 'wrongpass'}
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
