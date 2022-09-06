from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('marker', views.MarkerViewSet)
router.register('promise', views.PromiseViewSet)
router.register('marker-simple', views.MarkerSimpleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/v1/', include('accounts.urls')),
]