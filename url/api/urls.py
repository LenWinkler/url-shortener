from django.urls import path

from url.api import views

urlpatterns = [
    path('', views.create_url, name='create-url'),
    path('<existing_hash>/', views.retrieve_url, name='retrieve-url'),
]
