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

    def validate(self, data):
        """Validate that the info is entered correctly."""
        gender = data.get("gender", None)
        size = data.get("size", None)
        if gender not in ['m', 'f', 'u']:
            raise serializers.ValidationError(
                "Gender must be either 'm' for male, 'f' "
                "for female, or 'u' for unknown.")
        elif size not in ['s', 'm', 'l', 'xl', 'u']:
            raise serializers.ValidationError(
                "Size must be 's' for small, 'm' for medium, 'l' for large,"
                " 'xl' for extra large, or 'u' for unknown.")
        return data


class UserPrefSerializer(serializers.ModelSerializer):
    """The serializer for the UserPref model."""

    class Meta:
        """The fields for the UserPref model."""

        fields = (
            'age',
            'gender',
            'size')
        model = models.UserPref

    def validate(self, data):
        """Validate that the info is entered correctly."""
        age = data.get("age", None)
        age = age.split(",")
        size = data.get("size", None)
        size = size.split(",")
        gender = data.get("gender", None)
        gender = gender.split(",")
        for i in age:
            if i not in ['b', 'y', 'a', 's']:
                raise serializers.ValidationError(
                    "Age must be either 'b' for baby, 'y' for young,"
                    " 'a' for adult, or 's' for senior. Can do multiple with"
                    " commas, ex: a,y,e")
        for i in size:
            if i not in ['s', 'm', 'l', 'xl']:
                raise serializers.ValidationError(
                    "Size must be either 's' for small, 'm' for medium, 'l' "
                    "for large, or 'xl' for extra large. Can do multiple with"
                    " commas, ex: s,l,xl")
        for i in gender:
            if i not in ['m', 'f']:
                raise serializers.ValidationError(
                    "Gender must be either 'm' for male, or 'f' for female. Can"
                    " have both using commas, ex: m,f")
        return data


class FileSerializer(serializers.ModelSerializer):
    """The serializer for the File model to upload image."""

    class Meta():
        """Field for the File model."""

        model = models.File
        fields = ('file',)
