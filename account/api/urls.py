from django.urls import path

from account.api import views

urlpatterns = [
    path('register', views.registration_view, name='register'),
]