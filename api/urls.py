from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create, name='create'),
    path('<existing_hash>/', views.retrieve, name='retrieve'),
]