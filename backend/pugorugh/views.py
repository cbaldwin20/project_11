"""The views for the entire project."""

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
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

        # Get the variables to be used in filtering below.
        userpref = models.UserPref.objects.get(user=self.request.user)
        age = userpref.age.split(",")
        gender = userpref.gender.split(",")
        size = userpref.size.split(",")

        if response == 'liked':
            x = self.get_queryset().filter(
                dog__status='l', age_category__in=age,
                gender__in=gender, size__in=size)

            # now that we have the filtered dog instances
            # based on preferences,
            # we get the one that either is next in line
            # or if there is no next then go to the first
            # one.
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                return y
            else:
                return status.HTTP_404_NOT_FOUND

        elif response == 'disliked':
            x = self.get_queryset().filter(
                dog__status='d', age_category__in=age,
                gender__in=gender, size__in=size)

            # now that we have the filtered dog instances
            # based on preferences,
            # we get the one that either is next in line
            # or if there is no next then go to the first
            # one.
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                return y
            else:
                return status.HTTP_404_NOT_FOUND

        elif response == 'undecided':
            x = self.get_queryset().filter(
                age_category__in=age, gender__in=gender,
                size__in=size).exclude(dog__status__in=['l', 'd'])

            # now that we have the filtered dog instances
            # based on preferences,
            # we get the one that either is next in line
            # or if there is no next then go to the first
            # one.
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                return y
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

        dog_instance = self.get_queryset().get(id=pk)

        # if a UserDog instance exists then update it
        # if none exists then create one
        try:
            x = models.UserDog.objects.get(
                user=self.request.user, dog=dog_instance)
            x.status = response[0]
            x.save()
        except ObjectDoesNotExist:
            x = models.UserDog.objects.create(
                user=self.request.user, dog=dog_instance, status=response[0])
        dog = serializers.DogSerializer(dog_instance)
        return Response(dog.data)

    def delete(self, request, *args, **kwargs):
        """Delete a dog instance."""
        pk = self.kwargs.get('pk')
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
            x = self.get_queryset().get(user=self.request.user)
        except ObjectDoesNotExist:
            x = models.UserPref.objects.create(
                user=self.request.user, age='b', gender='m', size='s')
        return x


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
