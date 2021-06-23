from django.urls import path

from url.api.views import create_url, get_urls, retrieve_url

urlpatterns = [
    path('', create_url, name='create-url'),
    path('<existing_hash>/', retrieve_url, name='retrieve-url'),
    path('urls', get_urls, name='urls'),
]
