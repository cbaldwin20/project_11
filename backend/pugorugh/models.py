"""models for the entire project."""

from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    """model for a dog instance."""

    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField(help_text="integer for months")
    age_category = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=255,
        help_text='“m” for male, “f” for female, “u” for unknown"')
    size = models.CharField(
        max_length=255,
        help_text='"s" for small, "m" for medium, "l"'
        ' for large, "xl" for extra large, "u" for unknown')

    def save(self, *args, **kwarg):
        """Set the 'age_category' whenever the instance is saved."""
        if self.age < 25:
            self.age_category = "b"
        elif self.age < 50:
            self.age_category = "y"
        elif self.age < 75:
            self.age_category = "a"
        else:
            self.age_category = "s"
        super(Dog, self).save(*args, **kwarg)

    def __str__(self):
        """Return the dog name when instance is called."""
        return self.name


class UserDog(models.Model):
    """
    instance to determine whether a user

    liked, disliked, or undecided a dog instance.

    """

    user = models.ForeignKey(User, related_name="user")
    dog = models.ForeignKey(Dog, related_name="dog")
    status = models.CharField(
        max_length=255,
        help_text='“l” for liked, “d” for disliked')
    


class UserPref(models.Model):
    """preferences of what dog's the user likes."""

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

    


class File(models.Model):
    """an image to be used for a dog instance."""

    file = models.FileField(blank=False, null=False)
