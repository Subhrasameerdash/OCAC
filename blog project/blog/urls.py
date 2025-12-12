from django.urls import path

from .views import (
    MyPostListView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    RegisterView,
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/mine/', MyPostListView.as_view(), name='my_posts'),
    path('posts/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('register/', RegisterView.as_view(), name='register'),
]
