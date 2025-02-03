"""
    Tests for model.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email="user@xample.com", password="testpass123"):
    """ Helper function to create user that we use for assign to a tag. """
    return get_user_model().objects.create_user(email, password)

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

    def test_create_recipe(self):
        """Test creating a new recipe."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123',
        )
        """ user=user is the user who's recipe is belong to. """
        recipe = models.Recipe.objects.create(
            user = user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a new tag."""
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingrediant(self):
        """Test creating a new ingredient."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Cucumber',
        )

        self.assertEqual(str(ingredient), ingredient.name)
