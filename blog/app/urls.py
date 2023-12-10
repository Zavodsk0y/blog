from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsListView.as_view(), name='posts'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)