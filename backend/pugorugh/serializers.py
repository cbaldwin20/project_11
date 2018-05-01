"""the serializers for the entire project."""

from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """For the user model."""

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Create the user instance."""
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        """Gets the user model."""

        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    """The serializer for the Dog model."""

    class Meta:
        fields = (
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size',
            'id')
        model = models.Dog


class UserPrefSerializer(serializers.ModelSerializer):
    """The serializer for the UserPref model."""

    class Meta:
        """The fields for the UserPref model."""

        fields = (
            'age',
            'gender',
            'size')
        model = models.UserPref


class FileSerializer(serializers.ModelSerializer):
    """The serializer for the File model to upload image."""

    class Meta():
        """Field for the File model."""

        model = models.File
        fields = ('file',)
