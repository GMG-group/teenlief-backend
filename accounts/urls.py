from django.urls import path, include

urlpatterns = [
    path('v1/registration/', include('dj_rest_auth.registration.urls')),
]