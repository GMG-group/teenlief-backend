from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('marker', views.MarkerViewSet)
router.register('promise', views.PromiseViewSet)
router.register('marker-simple', views.MarkerSimpleViewSet)
router.register('tag', views.TagViewSet)
router.register('shelter', views.ShelterViewSet)
router.register('review', views.ReviewViewSet)
router.register('point', views.PointViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/v1/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('check-user-marker-exists/<int:user_id>/', views.CheckUserMarkerExistsAPI.as_view()),
    path('review/marker/list/', views.MarkerReviewListAPI.as_view()),
    # path('review/mypage/list'),
    # path('review/create'),
    # path('review/delete'),
]