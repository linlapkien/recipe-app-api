"""
Serializers for the user API View.
"""
from django.contrib.auth import ( get_user_model,
                                 authenticate )
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """
    """ Await convert object to Python Object. It takes JSON input that post from API, it validates the input and then converts it to a Python object or model use in the db. """
    class Meta:
        """ Meta class to define the fields that we want to pass to the model """
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    """ Override the create function to create a new user """
    """ This function is called when the validation is passed. """
    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update a user, setting the password correctly and return it """
        password = validated_data.pop('password', None)
        """ Call the ModelSerializer Baseclass update function """
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication token """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    """ Validate the input data """
    def validate(self, attrs):
        """ Validate and authenticate the user """
        """ Retrieve the email and password from the attrs that user provided in the input"""
        email = attrs.get('email')
        password = attrs.get('password')

        """ Authenticate the user """
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        """ If the user is not found, raise an error """
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        """ Set the user in the context """
        attrs['user'] = user
        return attrs
