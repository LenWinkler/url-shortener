from django.urls import path

from url.api.views import (create_url_view, get_urls_view, retrieve_url_view,
                            delete_url_view)

urlpatterns = [
    path('', create_url_view, name='create-url'),
    path('delete', delete_url_view, name='delete-url'),
    path('<existing_hash>/', retrieve_url_view, name='retrieve-url'),
    path('urls', get_urls_view, name='urls'),
]
