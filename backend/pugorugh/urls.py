from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', views.UserRegisterView.as_view(), name='register-user'),


    # get the next liked/disliked/undecided dog
    url(r'^api/dog/<pk>/liked/next/$', views.RetrieveUpdateDog.as_view()),
    url(r'^api/dog/<pk>/disliked/next/$', views.RetrieveUpdateDog.as_view()),
    url(r'^api/dog/<pk>/undecided/next/$', views.RetrieveUpdateDog.as_view()),

    # change the dog's status
    url(r'^api/dog/<pk>/liked/$', views.RetrieveUpdateDog.as_view()),
    url(r'^api/dog/<pk>/disliked/$', views.RetrieveUpdateDog.as_view()),
    url(r'^api/dog/<pk>/undecided/$', views.RetrieveUpdateDog.as_view()),
    

    # change or set user preferences
    url(r'^api/user/preferences/$', views.RetrieveUpdateUserPref.as_view()),
    url(r'^practice/<pk>/$', views.Practice.as_view()),

    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html'))
])

