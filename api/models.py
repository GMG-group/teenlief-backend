from django.db import models
from accounts.models import User


class Marker(models.Model):
    longitude = models.DecimalField(max_digits=20, decimal_places=10)  # 위도
    latitude = models.DecimalField(max_digits=20, decimal_places=10)  # 경도
    image = models.ImageField(blank=True, null=True, upload_to='images/')  # 사진
    explanation = models.TextField()  # 설명
    helper = models.ForeignKey(User, related_name='helper', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)  # 올린 시간


class promise(models.Model):
    teen = models.ForeignKey(User, related_name='teen', on_delete=models.SET_NULL)
    time = models.DateTimeField(blank=False)
    marker = models.ForeignKey(Marker, related_name='marker', on_delete=models.CASCADE, blank=False)
