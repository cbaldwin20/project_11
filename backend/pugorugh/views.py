from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, mixins
from rest_framework.generics import CreateAPIView

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

@api_view(['GET', 'PUT'])
def retrieve_update_userpref(request):
    try:
        myuserpref = models.UserPref.objects.get(user=request.user)
    except models.UserPref.DoesNotExist:
        myuserpref = models.UserPref.objects.create(
            user=User.objects.first(), age='b', gender='m', size='s')
    if request.method == 'GET':
        userpref_serialized = serializers.UserPrefSerializer(myuserpref)
        return Response(userpref_serialized.data)
    elif request.method == 'PUT':
            userpref_serialized = serializers.UserPrefSerializer(myuserpref, data=request.data)
            if userpref_serialized.is_valid():
                userpref_serialized.save()
                return Response(userpref_serialized.data)
            return Response(userpref_serialized.errors,
                status=status.HTTP_400_BAD_REQUEST)