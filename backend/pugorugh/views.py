"""The views for the entire project."""

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from . import serializers
from . import models

import logging
logging.basicConfig(filename="logging.log", level=logging.DEBUG)


class UserRegisterView(CreateAPIView):
    """View to register."""

    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogCreateAPIView(CreateAPIView):
    """Creates a dog instance."""

    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class RetrieveUpdateDestroyDog(generics.RetrieveUpdateDestroyAPIView):
    """Can get, update, or delete a dog instance."""

    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self, *args, **kwargs):
        """Get the object to be returned in the GET request."""
        # getting the parameters from the url
        response = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')
        pk = int(pk)

        # Get the variables to be used in filtering below.
        userpref = models.UserPref.objects.get(user=self.request.user)
        age = userpref.age.split(",")
        gender = userpref.gender.split(",")
        size = userpref.size.split(",")

        if response == 'liked':
            liked_dogs = self.get_queryset().filter(
                dog__status='l', age_category__in=age,
                gender__in=gender, size__in=size,
                dog__user=self.request.user)

            # now that we have the filtered dog instances
            # based on preferences,
            # we get the one that either is next in line
            # or if there is no next then go to the first
            # one.
            if liked_dogs:
                try:
                    liked_dog = liked_dogs.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    liked_dog = liked_dogs.first()
                return liked_dog
            else:
                return status.HTTP_404_NOT_FOUND

        elif response == 'disliked':
            disliked_dogs = self.get_queryset().filter(
                dog__status='d', age_category__in=age,
                gender__in=gender, size__in=size,
                dog__user=self.request.user)

            # now that we have the filtered dog instances
            # based on preferences,
            # we get the one that either is next in line
            # or if there is no next then go to the first
            # one.
            if disliked_dogs:
                try:
                    disliked_dog = disliked_dogs.filter(
                        id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    disliked_dog = disliked_dogs.first()
                return disliked_dog
            else:
                return status.HTTP_404_NOT_FOUND

        elif response == 'undecided':
            # if this user is new, then create a UserDog
            # instance for every Dog instance.
            if pk < 0:
                any_userdogs = models.UserDog.objects.filter(
                    user=self.request.user).exists()
                if not any_userdogs:
                    all_dogs = models.Dog.objects.all()
                    for dog in all_dogs:
                        models.UserDog.objects.create(
                            user=self.request.user,
                            dog=dog,
                            status="u")

            undecided_dogs = self.get_queryset().filter(
                age_category__in=age, gender__in=gender,
                size__in=size, dog__user=self.request.user,
                dog__status='u')

            # now that we have the filtered dog instances
            # based on preferences,
            # we get the one that either is next in line
            # or if there is no next then go to the first
            # one.
            if undecided_dogs:
                try:
                    undecided_dog = undecided_dogs.filter(
                        id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    undecided_dog = undecided_dogs.first()
                return undecided_dog
            else:
                return status.HTTP_404_NOT_FOUND
        else:
            return status.HTTP_404_NOT_FOUND

    def put(self, request, *args, **kwargs):
        """Create a UserDog instance which

        decides if you liked/disliked/undecided.
        """
        # gets the url parameters
        response = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')
        pk = int(pk)

        dog_instance = self.get_queryset().get(id=pk)

        # if a UserDog instance exists then update it
        # if none exists then create one

        my_userdog = models.UserDog.objects.get(
            user=self.request.user, dog=dog_instance)
        my_userdog.status = response[0]
        my_userdog.save()

        dog = serializers.DogSerializer(dog_instance)
        return Response(dog.data)

    def delete(self, request, *args, **kwargs):
        """Delete a dog instance."""
        pk = self.kwargs.get('pk')
        pk = int(pk)
        dog = get_object_or_404(models.Dog, id=pk)
        try:
            userdog = models.UserDog.objects.get(
                dog=dog, user=self.request.user)
            userdog.delete()
        except ObjectDoesNotExist:
            pass
        dog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveUpdateUserPref(generics.RetrieveUpdateAPIView):
    """Get and update the user preferences."""

    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self, *args, **kwargs):
        """Will get the UserPref to use."""
        # will try to get the UserPref instance for this user,
        # but if there is none we create one to be soon after
        # updated with a 'PUT'.
        try:
            my_userpref = self.get_queryset().get(user=self.request.user)
        except ObjectDoesNotExist:
            my_userpref = models.UserPref.objects.create(
                user=self.request.user, age='b', gender='m', size='s')
        return my_userpref


class FileView(APIView):
    """Add an image to the static/images/dogs folder."""

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """Post an image."""
        file_serializer = serializers.FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(
                file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
