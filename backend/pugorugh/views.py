from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, mixins
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User
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
 


 
class ListCreateUserPref(generics.ListCreateAPIView):
    queryset = models.UserPref.objects.all() 
    serializer_class = serializers.UserPrefSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDog(generics.RetrieveUpdateAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer 

# my 'get_object' will have to get the dog with a pk
# greater than the given pk. 
# then on the 'PUT' I need to update/create the 'models.UserDog' to
# be either 'liked' or 'disliked' 
    # def get_object(self, *args, **kwargs):
    #     try:
    #         x = self.get_queryset().get(user=self.request.user)
    #     except ObjectDoesNotExist:
    #         x = models.UserPref.objects.create(user=self.request.user,
    #             age='b', gender='m', size='s')
    #     return x
    
    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=1)





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


class Practice(APIView):
    def get(self, request, pk, format=None):
        x = get_object_or_404(models.Dog, id=int(pk))
        y = serializers.DogSerializer(x)
        return Response(y.data)

    

    