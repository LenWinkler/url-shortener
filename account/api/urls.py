from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from account.api import views

urlpatterns = [
    path('register', views.registration_view, name='register'),
    path('login', obtain_auth_token, name='register'),
]
