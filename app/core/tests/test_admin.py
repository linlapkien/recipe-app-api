"""
Tests for the Djangois admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Test for Django admin. """

    def setUp(self):
        """ Create user and Client. """
        """ Frist, we create a superuser. And then we create a client. And then we create test regularily user in the database. """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password123',
            name='Test User',
        )

    """ Reverse document: https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#:~:text=they%20were%20logged.-,Reversing%20admin%20URLs,-%C2%B6"""
    def test_users_listed(self):
        """Test that users are listed on user page."""
        """ A unit Test for the user lists. """
        """ admin:core_user_changelist is the url that pull from the django admin. """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        """ assertContains: Check the page contains the value. """
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that the user edit page works."""
        """ admin:core_user_change, this is url for the change user page, and we need to pass specific id to change the user. """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        """Ensure that the page is working. So, we check the HTTP status code is 200."""
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works."""
        """ admin:core_user_add is the url for the create user page. """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
