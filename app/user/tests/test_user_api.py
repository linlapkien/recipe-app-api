"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
""" URL endpoint we gonna add for creating a new token """
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

""" Generic params, used in tests """
def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test the users API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        """ post payload to the create user API """
        res = self.client.post(CREATE_USER_URL, payload)

        """ assert that the response status code is 201 (201 created successfull response) """
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        """ check the user object from the database """
        user = get_user_model().objects.get(email=payload['email'])
        """ Verifies the password was hashed (as check_password will validate the hash, not the plaintext password)."""
        self.assertTrue(user.check_password(payload['password']))
        """ the API does not return sensitive data like the user's password in the response payload."""
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test creating a user that already exists => fails """
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        """ New user but email already exists in db => (400 bad request) """
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Test that the password must be more than 5 characters """
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        """ user_exists return boolean """
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        """ If user_exists return found => user does not exist """
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test that a token is created for valid credentials. """
        """ First, Create a new user """
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123'
        }
        create_user(**user_details)

        """ Then, Create a payload that have email and pw """
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        """ Then, Post the payload to the token url API """
        res = self.client.post(TOKEN_URL, payload)

        """ Check if the token is in the response data """
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test returns error if credentials invalids """
        create_user(
            email='test@#example.com',
            password='goodpassword'
        )

        payload = {
            'email': 'test@example.com',
            'password': 'badpassword'
        }
        res = self.client.post(TOKEN_URL, payload)

        """ bad credentials so we don't expect a token in res.data this time. So token will not be generated"""
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test posting a blank password returns an error """
        payload = {
            'email': 'test@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API requests that require authentication """
    """ We have existing user in the db, so we can use it for testing """
    def setUp(self):
        self.user = create_user(
            email = 'test@example.com',
            password = 'testpass123',
            name = 'Test Name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """ Test that POST is not allowed on the me URL """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """
        payload = {'name': 'new name', 'password': 'newpassword123'}
        """ Patch request to update the ME_URL with the payload """
        res = self.client.patch(ME_URL, payload)
        """ Refresh the user object from the db, By defaults, they will not refresh automatically """
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
