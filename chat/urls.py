from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat import views


router = DefaultRouter()
router.register('', views.ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test', views.index, name='index'),
    path('test/<str:room_name>/', views.room, name='room'),
]
