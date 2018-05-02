"""Tests for the entire project."""

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token

from . import models


class PughorUghViewsFile(APITestCase):
    """Testing my views.py file."""

    def setUp(self):
        """Create instances for each model in project."""
        self.client = APIClient()

        self.user_one = User.objects.create_user(
            username='user_one',
            email='user_one@gmail.com',
            password='user_one')

        self.dog_one = models.Dog.objects.create(
            name='George',
            image_filename='pitbull.jpg',
            breed='pitbull',
            age=20,
            gender='m',
            size='s')

        self.userpref_one = models.UserPref.objects.create(
            user=self.user_one,
            age='b',
            gender='m',
            size='s')

        self.userdog_one = models.UserDog.objects.create(
            user=self.user_one,
            dog=self.dog_one,
            status='l')

        self.token = Token.objects.create(user=self.user_one)

    def test_register_user(self):
        """Test that we can create a user."""
        self.client.post(reverse('backend:register-user'),
                         {'username': 'user_two',
                         'password': 'user_two'})

        user_two = User.objects.get(username='user_two')
        self.assertTrue(user_two)

    def test_dog_create_not_authorized(self):
        """We should be blocked from creating a dog instance."""
        response = self.client.post(reverse('backend:create'),
                                    {
                                    'name': 'Mikey',
                                    'image_filename': 'chihuahua.jpg',
                                    'breed': 'chihuahua',
                                    'age': 40,
                                    'gender': 'm',
                                    'size': 's'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dog_create(self):
        """Create a dog instance."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post(reverse('backend:create'),
                         {
                         'name': 'Mikey',
                         'image_filename': 'chihuahua.jpg',
                         'breed': 'chihuahua',
                         'age': 40,
                         'gender': 'm',
                         'size': 's'})
        new_dog = models.Dog.objects.get(name="Mikey")
        self.assertEqual(new_dog.name, 'Mikey')

    def test_retrieve_userpref_not_authorized(self):
        """Should not be able to retrieve userpref instance."""
        response = self.client.get(reverse('backend:userpref'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_userpref(self):
        """Retrive our userpref instance."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('backend:userpref'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_userpref(self):
        """Update the userpref instance."""
        self.assertTrue(self.userpref_one.age, 'b')
        self.client.put(reverse('backend:userpref'),
                        {'user': self.user_one,
                        'age': 'y',
                         'gender': 'm',
                         'size': 's'})
        self.assertTrue(self.userpref_one.age, 'y')

    def test_get_next_liked_dog_not_authorized(self):
        """Should be blocked from getting next liked dog."""
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': 5, 'decision': 'liked'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': -1, 'decision': 'liked'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_next_liked_dog(self):
        """Getting the next liked dog instance."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': 5, 'decision': 'liked'}))
        self.assertEqual(response.data['name'], 'George')
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': -1, 'decision': 'liked'}))
        self.assertEqual(response.data['name'], 'George')

    def test_get_next_disliked_dog_not_authorized(self):
        """Should be blocked from getting next disliked dog."""
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': 5, 'decision': 'disliked'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': -1, 'decision': 'disliked'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_next_disliked_dog(self):
        """Get the next disliked dog."""
        userdog = models.UserDog.objects.first()
        userdog.status = 'd'
        userdog.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': 5, 'decision': 'disliked'}))
        self.assertEqual(response.data['name'], 'George')
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': -1, 'decision': 'disliked'}))
        self.assertEqual(response.data['name'], 'George')

    def test_get_next_undecided_dog_not_authorized(self):
        """Should be blocked from getting the next undecided dog."""
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': 5, 'decision': 'undecided'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': -1, 'decision': 'undecided'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_next_undecided_dog(self):
        """Get next undecided dog."""
        userdog = models.UserDog.objects.first()
        userdog.status = 'u'
        userdog.save()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': 5, 'decision': 'undecided'}))
        self.assertEqual(response.data['name'], 'George')
        response = self.client.get(reverse(
            'backend:next', kwargs={'pk': -1, 'decision': 'undecided'}))
        self.assertEqual(response.data['name'], 'George')

    def test_update_userdog(self):
        """Update the userdog instance using 'd', 'l', and other."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        id = self.userdog_one.id
        self.client.put(reverse('backend:update', args=[id, 'disliked']),
                        {'user': self.user_one,
                        'dog': self.dog_one,
                         'status': 'd'})
        userdog = models.UserDog.objects.get(id=id)
        self.assertEqual(userdog.status, 'd')

        self.client.put(reverse('backend:update', args=[id, 'liked']),
                        {'user': self.user_one,
                        'dog': self.dog_one,
                         'status': 'l'})
        userdog = models.UserDog.objects.get(id=id)
        self.assertEqual(userdog.status, 'l')

        self.client.put(reverse('backend:update', args=[id, 'undecided']),
                        {'user': self.user_one,
                        'dog': self.dog_one,
                         'status': 'd'})
        userdog = models.UserDog.objects.get(id=id)
        self.assertNotEqual(userdog.status, 'l')
        self.assertNotEqual(userdog.status, 'd')

    def test_delete_dog_not_authorized(self):
        """Should be blocked from deleting a dog instance."""
        id = self.userdog_one.id
        response = self.client.delete(reverse(
            'backend:update', args=[id, 'delete']),
            {'user': self.user_one,
             'dog': self.dog_one,
             'status': 'd'})
        dog = models.Dog.objects.filter(id=id)
        userdog = models.UserDog.objects.filter(id=id)
        self.assertTrue(dog)
        self.assertTrue(userdog)
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_dog(self):
        """Delete a dog instance."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        id = self.userdog_one.id
        response = self.client.delete(reverse(
            'backend:update', args=[id, 'delete']),
            {'user': self.user_one,
             'dog': self.dog_one,
             'status': 'd'})
        dog = models.Dog.objects.filter(id=id)
        userdog = models.UserDog.objects.filter(id=id)
        self.assertFalse(dog)
        self.assertFalse(userdog)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
