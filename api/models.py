from django.db import models
from accounts.models import User
from django.utils import timezone
from uuid import uuid4

def date_upload_to(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = '.jpeg'
    # 결합 후 return
    return '/'.join([
        'images',
        ymd_path,
        uuid_name + extension,
        ])

class Tag(models.Model):
    tag = models.CharField(max_length=20)


class Marker(models.Model):
    longitude = models.DecimalField(max_digits=20, decimal_places=15)  # 위도
    latitude = models.DecimalField(max_digits=20, decimal_places=15)  # 경도
    image = models.FileField(blank=True, null=True, upload_to=date_upload_to, max_length=300)  # 사진
    explanation = models.TextField()  # 설명
    helper = models.ForeignKey(User, related_name='helper', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)  # 올린 시간


class Promise(models.Model):
    teen = models.ForeignKey(User, related_name='teen', on_delete=models.CASCADE)
    time = models.DateTimeField(blank=False)
    marker = models.ForeignKey(Marker, related_name='promises', on_delete=models.CASCADE, blank=False)
