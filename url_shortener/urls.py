from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('url.api.urls')),
    path('account/api/', include('account.api.urls')),
]
