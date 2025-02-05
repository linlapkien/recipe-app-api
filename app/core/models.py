"""
Databases Models.
"""
import uuid
import os

from django.conf import settings
from django.db import models # noqa
""" https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.get_username:~:text=Importing-,AbstractBaseUser,-AbstractBaseUser%20and%20BaseUserManager """ # noqa
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin ) # noqa


def recipe_image_file_path(instance, filename):
    """ Generate file path for new recipe image. """
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads' ,'recipe', filename)

class UserManager(BaseUserManager):
    """ Manager for user."""

    def create_user(self, email, password=None, **extra_fields):
        """ Creatre, save and return a new user """
        if not email:
            raise ValueError('Users must have an email address.')
        """Pass normalised email to the email field. be4 saving the user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        """ This set_password will encrypt the password. """
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create and save a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


""" PermissionsMixin = Functioonality for the permiussions & fields. """
class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    """ is_staff, Login with django admin """
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Recipe(models.Model):
    """ Recipe object. """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title

class Tag(models.Model):
    """ Tag to be used for a recipe. """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """ Ingredient to be used in a recipe. """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name