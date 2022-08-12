from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/v1/', include('accounts.urls')),
]