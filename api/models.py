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
    STATUS = (
        ('A', 'AVILABLE'),
        ('D', 'DELETED'),
    )

    longitude = models.DecimalField(max_digits=20, decimal_places=15)  # 위도
    latitude = models.DecimalField(max_digits=20, decimal_places=15)  # 경도
    address = models.CharField(max_length=255)  # 주소
    image = models.FileField(blank=True, null=True, upload_to=date_upload_to, max_length=300)  # 사진
    explanation = models.TextField()  # 설명
    helper = models.ForeignKey(User, related_name='helper', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)  # 올린 시간
    status = models.CharField(max_length=1, choices=STATUS, default='A')


class Promise(models.Model):
    teen = models.ForeignKey(User, related_name='promise_teen', on_delete=models.CASCADE)
    helper = models.ForeignKey(User, related_name='promise_helper', on_delete=models.CASCADE)
    time = models.DateTimeField(blank=False)
    marker = models.ForeignKey(Marker, related_name='promises', on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    reviewed = models.BooleanField(default=False)


class Shelter(models.Model):
    longitude = models.DecimalField(max_digits=20, decimal_places=15)  # 위도
    latitude = models.DecimalField(max_digits=20, decimal_places=15)  # 경도
    phone_number = models.CharField(max_length=20, null=True)
    explanation = models.TextField()  # 설명
    name = models.CharField(max_length=255)


class Review(models.Model):
    author = models.ForeignKey(User, related_name='review_author', on_delete=models.CASCADE)
    helper = models.ForeignKey(User, related_name='review_helper', on_delete=models.SET_NULL, null=True)
    promise = models.OneToOneField(Promise, related_name="review_promise", on_delete=models.PROTECT)
    stars = models.DecimalField(max_digits=3, decimal_places=2)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.author)


class PointLog(models.Model):
    sender = models.ForeignKey(User, related_name='point_log_sender', on_delete=models.PROTECT)
    receiver = models.ForeignKey(User, related_name='point_log_receiver', on_delete=models.PROTECT)
    point = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class HelperInfo(models.Model):
    helper = models.OneToOneField(User, related_name="helper_info_helper", on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=3, decimal_places=2)
    review_count = models.IntegerField()
    total = models.DecimalField(max_digits=20, decimal_places=2)


class CertificateCode(models.Model):
    """
    status: [
        VE: 인증 성공
        DE: 인증 실패
        CR: 인증 예정
    ]
    """
    user = models.ForeignKey(User, related_name='certificate_user', on_delete=models.PROTECT)
    expire_date = models.DateTimeField()
    status = models.CharField(max_length=2)
    code = models.CharField(max_length=6)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1)
