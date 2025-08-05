"""Defines URL patterns for accounts."""
from django.urls import path, include
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')), # look reset url, reset done url, etc...
    path('register/', views.register, name='register')
]