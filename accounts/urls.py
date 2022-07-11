from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('allauth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('login/google/finish/', views.GoogleLogin.as_view(), name='google_login_finish'),
    path('login/google/', views.google_login, name='google_login'),
    path('login/google/callback/', views.google_callback, name='google_callback'),
]

# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/api/accounts/google/login/callback/&prompt=consent&response_type=code&client_id=674602775271-jtr4bh5savtt9p4q1shuieiqlt1l18dp.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline
# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://127.0.0.1:8000/api/accounts/v1/google/login/callback/&prompt=consent&response_type=token&client_id=674602775271-jtr4bh5savtt9p4q1shuieiqlt1l18dp.apps.googleusercontent.com&scope=openid%20email%20profile