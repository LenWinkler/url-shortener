from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from account.api.views import (registration_view, account_properties_view,
                                update_account_view, delete_account_view)

urlpatterns = [
    path('delete', delete_account_view, name='delete'),
    path('login', obtain_auth_token, name='register'),
    path('properties', account_properties_view, name='properties'),
    path('properties/update', update_account_view, name='update'),
    path('register', registration_view, name='register'),
]
