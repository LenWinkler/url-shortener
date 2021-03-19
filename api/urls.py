from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_info),
    path('create/', views.create_url, name='create-url'),
    path('<existing_hash>/', views.retrieve_url, name='retrieve-url'),
]