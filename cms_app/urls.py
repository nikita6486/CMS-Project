from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('posts/', PostListCreateAPIView.as_view(), name='post-list'),
    path('posts_RUD/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-get'),
    path('posts_RUD/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('likes/', LikeCreateAPIView.as_view(), name='like-create'),
    path('likes/<int:pk>/', LikeRetrieveUpdateDestroyAPIView.as_view(), name='like-detail'),

    path('list_users/', UserListAPIView.as_view(), name='list_users'),
    path('update_users/', UpdateUserView.as_view(), name='update-user'),
    path('delete_users/', DeleteUserView.as_view(), name='delete-user'),

    
]