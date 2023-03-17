from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import User

class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    @patch('register.views.jwt')
    def test_register_view(self, mock_jwt):
        mock_jwt.encode.return_value = 'fake_token'

        # make a POST request to the view with valid user data
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')

        # assert that the response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # assert that the response contains the expected user ID
        self.assertEqual(response.data['user_id'], 1)  # assuming this is the first user created in the database

        # assert that the response contains the expected access token and refresh token
        self.assertEqual(response.data['tokens']['access_token'], 'fake_token')
        self.assertEqual(response.data['tokens']['refresh_token'], 'fake_token')

        # assert that the User object was created with the correct username and email
        self.assertEqual(response.data['user_id'], User.objects.first().id)
        self.assertEqual(User.objects.first().username, 'testuser')
        self.assertEqual(User.objects.first().email, 'testuser@example.com')
