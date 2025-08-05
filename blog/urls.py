"""Defines URL patterns for blog."""
from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('my_blogs/', views.my_blogs, name='my_blogs'),
    path('new_blog/', views.new_blog, name='new_blog'),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('posts/<int:blog_id>/', views.posts, name='posts'),
    path('new_post/<int:blog_id>/', views.new_post, name='new_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]