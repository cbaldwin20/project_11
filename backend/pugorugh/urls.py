"""Urls for the entire project."""

from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', views.UserRegisterView.as_view(),
        name='register-user'),

    # these are all the 'GET' requests, liked/disliked/undecided
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<decision>liked|disliked|undecided)/next/$',
        views.RetrieveUpdateDestroyDog.as_view(), name="next"),

    # these are all the 'PUT' requests, liked/disliked/undecided/delete
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<decision>liked|disliked|undecided|delete)/$',
        views.RetrieveUpdateDestroyDog.as_view(), name="update"),

    # change or set user preferences
    url(r'^api/user/preferences/$', views.RetrieveUpdateUserPref.as_view(),
        name='userpref'),

    # use this to create a dog instance.
    url(r'^api/dog/create/$', views.DogCreateAPIView.as_view(), name='create'),

    # use this url to upload an image.
    url(r'^file/upload/$', views.FileView.as_view(), name='file-upload'),

    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html'))
])
