
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, mixins
from rest_framework.generics import CreateAPIView

from . import serializers
from . import models

import logging
logging.basicConfig(filename="logging.log", level=logging.DEBUG)


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer

class ListCreateDog(generics.ListCreateAPIView):
    queryset = models.Dog.objects.all() 
    serializer_class = serializers.DogSerializer
 
class RetrieveUpdateDestroyDog(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer 

 
class ListCreateUserPref(generics.ListCreateAPIView):
    queryset = models.UserPref.objects.all() 
    serializer_class = serializers.UserPrefSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
 
class RetrieveUpdateUserPref(generics.RetrieveUpdateAPIView):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self, *args, **kwargs):
        try:
            x = self.get_queryset().get(user=self.request.user)
        except ObjectDoesNotExist:
            x = models.UserPref.objects.create(user=self.request.user,
                age='b', gender='m', size='s')
        return x
