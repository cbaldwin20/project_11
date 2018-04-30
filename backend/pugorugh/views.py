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
    
    def get_object(self, *args, **kwargs):
        response = self.kwargs.get('decision')
        pk = self.kwargs.get('pk')
        
        if response == 'liked':
            x = self.get_queryset().filter(dog__status='l')
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                    # dog.dog.status
                    # Dog.objects.exclude(subject__in=['l', 'd'])
                    # Dog.objects.filter(teacher__username=teacher)
                    # x.filter(id__gt=1)[:1].get()
                return y
            else:
                return status.HTTP_404_NOT_FOUND
        
        elif response == 'disliked':
            x = self.get_queryset().filter(dog__status='d')
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                    # dog.dog.status
                    # Dog.objects.exclude(subject__in=['l', 'd'])
                    # Dog.objects.filter(teacher__username=teacher)
                    # x.filter(id__gt=1)[:1].get()
                return y
            else:
                return status.HTTP_404_NOT_FOUND
        
        elif response == 'undecided':
            x = self.get_queryset().exclude(dog__status__in=['l', 'd'])
            if x:
                try:
                    y = x.filter(id__gt=pk)[:1].get()
                except ObjectDoesNotExist:
                    y = x.first()
                    # dog.dog.status
                    # Dog.objects.exclude(subject__in=['l', 'd'])
                    # Dog.objects.filter(teacher__username=teacher)
                    # x.filter(id__gt=1)[:1].get()
                return y
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

# for 'undecided', get all of the models.Dog that have no UserDog, then
# has a pk larger than the pk given. Then choose the one with the smallest pk.
# if there is none with a larger pk, then go to the 'first()' one.
# if there is none at all then return a 404. 
# ***basically do a try on the ones with greater than pk, if that doesn't work
# then in the except see if there are any at all with any pk or throw a 404

# for 'liked', get all the models.Dog with a UserDog that has a status of 'liked',
# and has a greater than pk than the one given. Then get the one with the smallest pk. 
# if there is none with a pk greater, then go back to the first() one. 





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




    

    
# so just do a retrieve for the 'liked', 'disliked', 'undecided'
# then for the 'PUT' have it find/create a 'UserDog' for the 'Dog' instance. 