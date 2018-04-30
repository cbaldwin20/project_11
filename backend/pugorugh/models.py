from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField(help_text="integer for months")
    gender = models.CharField(
        max_length=255,
        help_text='“m” for male, “f” for female, “u” for unknown"')
    size = models.CharField(
        max_length=255,
        help_text='"s" for small, "m" for medium, "l"'
        ' for large, "xl" for extra large, "u" for unknown')

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, related_name="user")
    dog = models.ForeignKey(Dog, related_name="dog")
    status = models.CharField(
        max_length=255,
        help_text='“l” for liked, “d” for disliked')

    def __str__(self):
        return self.user


class UserPref(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)
    age = models.CharField(
        max_length=255,
        help_text='“b” for baby, “y” for'
        ' young, “a” for adult, “s” for senior')
    gender = models.CharField(
        max_length=255,
        help_text='“m” for male, “f” for female')
    size = models.CharField(
        max_length=255,
        help_text='“s” for small, “m” for medium, '
        '“l” for large, “xl” for extra large')

    def __str__(self):
        return self.user
