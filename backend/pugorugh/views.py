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


class DogCreateAPIView(CreateAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class RetrieveUpdateDestroyDog(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer 


    
    def get_object(self, *args, **kwargs):
        response = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')

        userpref = models.UserPref.objects.get(user=self.request.user)
        age = userpref.age.split(",")
        gender = userpref.gender.split(",")
        size = userpref.size.split(",")
        
        if response == 'liked':
            x = self.get_queryset().filter(dog__status='l', age_category__in=age, gender__in=gender, size__in=size)
            
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                return y
            else:
                return status.HTTP_404_NOT_FOUND
        
        elif response == 'disliked':
            x = self.get_queryset().filter(dog__status='d', age_category__in=age, gender__in=gender, size__in=size)
            
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                return y
            else:
                return status.HTTP_404_NOT_FOUND
        
        elif response == 'undecided':
            x = self.get_queryset().filter(age_category__in=age, gender__in=gender, size__in=size).exclude(dog__status__in=['l', 'd'])
            
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
        response = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')
        dog_instance = self.get_queryset().get(id=pk)
        try:
            x = models.UserDog.objects.get(user=self.request.user, dog=dog_instance)
            x.status = response[0]
            x.save()
        except ObjectDoesNotExist:
            x = models.UserDog.objects.create(user=self.request.user, dog=dog_instance, status=response[0])
        dog = serializers.DogSerializer(dog_instance)
        return Response(dog.data)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        dog = get_object_or_404(models.Dog, id=pk)
        try:
            userdog = models.UserDog.objects.get(dog=dog, user=self.request.user)
            userdog.delete()
        except ObjectDoesNotExist:
            pass
        dog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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




    

  