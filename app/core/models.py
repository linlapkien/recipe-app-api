"""
Databases Models.
"""
from django.db import models
""" #https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.get_username:~:text=Importing-,AbstractBaseUser,-AbstractBaseUser%20and%20BaseUserManager """
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """ Manager for user."""

    def create_user(self, email, password=None, **extra_fields):
        """ Creatre, save and return a new user """
        if not email:
            raise ValueError('Users must have an email address.')
        """ Pass normalised email to the email field. before saving the user. """
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
