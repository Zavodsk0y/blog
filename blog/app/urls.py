from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
                  path('login/', BBLoginView.as_view(), name='login'),
                  path('logout/', BBLogoutView.as_view(), name='logout'),
                  path('', PostsListView.as_view(), name='posts'),
                  path('create_profile', CreateProfileView.as_view(), name='create_profile'),
                  path('<int:pk>/profile', ProfileDetailView.as_view(), name='profile'),
                  path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
                  path('delete_profile/', DeleteProfileView.as_view(), name='delete_profile'),
                  path('create_post/', CreatePostView.as_view(), name='create_post'),
                  path('create_comment/', CreateCommentView.as_view(), name='create_comment'),
                  path('<int:pk>/edit_comment', EditCommentView.as_view(), name='edit_comment'),
                  path('<int:pk>/delete_comment', DeleteCommentView.as_view(), name='delete_comment'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
