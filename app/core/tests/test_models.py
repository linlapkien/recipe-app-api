"""
    Tests for model.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models. """

    def test_create_user_with_email_sucessful(self):
        """Test creationg a user with an email is successfull."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized. We define list of sample emails and expected emails. And we literating list of sample emails and creating user with sample email. And we are checking the email is normalized or not. """
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            """ We not testing the password here. So i will pass the password as sample123. """
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        """ Field provided by PermissionsMixin """
        """ In order to access Django admin, is_staff be True. Allow you to login to Django admin.  superuser is_superuser be True. allow you to access everything insite Django admin. """
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
