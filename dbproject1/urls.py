from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('listings.urls')),
    path('', include('contacts.urls')),
    path('', include('posts.urls')),
] 