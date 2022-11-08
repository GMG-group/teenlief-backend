import datetime
import pytz
import random

from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
# from teenlief-backend.api.serializers import ReviewSerializer
from rest_framework.generics import get_object_or_404

from accounts.models import User
from accounts.serializers import UserSerializer
from api.models import Marker, Promise, Tag, Shelter, Review, PointLog, HelperInfo, CertificateCode
from api.serializers import MarkerSerializer, PromiseSerializer, MarkerSimpleSerializer, TagSerializer, \
    ReviewSerializer, \
    ShelterSerializer, PointSerializer, MyMarkerSerializer, HelperInfoSerializer

from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from twilio.rest import Client

from teenlief.settings import get_env_variable


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(status='A')

    def perform_create(self, serializer):
        serializer.save(helper=self.request.user)

    def perform_destroy(self, instance):
        instance.status = 'D'
        instance.save()

    @action(detail=False, methods=['get'])
    def my(self, request):
        serializer_class = MyMarkerSerializer
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(helper=user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True, context={
            'request': request})  # context 안붙이면 full url로 안나옴 https://stackoverflow.com/a/69900733
        return Response(serializer.data)


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer

    def perform_create(self, serializer):
        serializer.save(helper=self.request.user)

    @action(detail=False, methods=['get'])
    def unreviewed(self, request):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(Q(teen=user) & Q(reviewed=False)))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True, context={
            'request': request})  # context 안붙이면 full url로 안나옴 https://stackoverflow.com/a/69900733
        return Response(serializer.data)


class MarkerSimpleViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSimpleSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ShelterViewSet(viewsets.ModelViewSet):
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer


class CheckUserMarkerExistsAPI(APIView):
    def get(self, request, user_id):
        marker = Marker.objects.filter(helper_id=user_id)
        if marker.exists():
            return Response(marker[0].id)
        else:
            return Response(False)


class PointViewSet(viewsets.ModelViewSet):
    queryset = PointLog.objects.all()
    serializer_class = PointSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sender = get_object_or_404(User, id=self.request.data["sender"])
        receiver = get_object_or_404(User, id=self.request.data["receiver"])
        point = int(self.request.data["point"])

        serializer = self.get_serializer(data=self.request.data)

        if self.request.user == sender:
            if sender == receiver:
                if serializer.is_valid():
                    serializer.save(sender=sender, receiver=receiver, point=point)
                    receiver.point += point
                    receiver.save()
            else:
                if sender.point >= point:
                    if serializer.is_valid():
                        serializer.save(sender=sender, receiver=receiver, point=point)
                        sender.point -= point
                        sender.save()
                        receiver.point += point
                        receiver.save()
                else:
                    return Response(False)

            return Response(serializer.data)
        return Response(False, status=403)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request):
        queryset = Review.objects.filter(author=self.request.user)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def my(self, request):
        user = request.user
        if user.role == "Helper":
            queryset = self.filter_queryset(self.get_queryset().filter(helper=user))
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(author=user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True, context={
            'request': request})  # context 안붙이면 full url로 안나옴 https://stackoverflow.com/a/69900733
        return Response(serializer.data)


class HelperInfoViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = HelperInfo.objects.all()
    serializer_class = HelperInfoSerializer

    def retrieve(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        queryset = HelperInfo.objects.get(helper=user)
        serializer = HelperInfoSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CertificateAPI(APIView):
    def post(self, request, *args, **kwargs):
        if request.user:
            user_certificate_data = CertificateCode.objects.filter(user=request.user, status="CR")
            if user_certificate_data:
                user_certificate_data = user_certificate_data.first()
                if user_certificate_data.status != 'DE':
                    user_certificate_data.status = 'DE'
                    user_certificate_data.save()

            # 6자리 랜덤 문자 생성
            random_string = [str(random.randint(0, 9)) for _ in range(6)]
            random_string = "".join(random_string)

            user = request.user
            code = random_string
            expire_date = datetime.datetime.now() + datetime.timedelta(minutes=3) + datetime.timedelta(hours=9)
            phone = request.data['phone']
            gender = request.data['gender']

            # 인증 관련 정보를 db에 추가
            CertificateCode.objects.create(user=user, code=code, expire_date=expire_date, status='CR', phone=phone, gender=gender)

            account_sid = get_env_variable("TWILIO_SID")
            auth_token = get_env_variable("TWILIO_TOKEN")
            client = Client(account_sid, auth_token)

            try:
                client.messages.create(
                    body=f'Your verification code is {code}',
                    from_='+18085152411',
                    to=f'+82{phone}'
                )
            except:
                return Response({"status": "TWILIO_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "success"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class VerifyCertificateAPI(APIView):
    def post(self, request, *args, **kwargs):
        if request.user:
            user = request.user
            receved_code = request.data['code']
            user_certificate_data = CertificateCode.objects.filter(user=request.user, status="CR").first()

            if user_certificate_data:
                expire_date = user_certificate_data.expire_date
                from django.utils import timezone
                now = timezone.now() + datetime.timedelta(hours=9)

                print(expire_date, now)
                if user_certificate_data.code == receved_code and expire_date >= now:
                    user_certificate_data.status = 'VE'
                    user_certificate_data.save()

                    user.certificated = True
                    user.phone_number = user_certificate_data.phone
                    user.gender = user_certificate_data.gender
                    user.save()

                    return Response({"status": "VERIFY_SUCCESS"}, status=status.HTTP_200_OK)

                else:
                    return Response({"status": "CODE_EXPIRED"}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"status": "NO_CERTIFICATE_DATA_IN_DB"}, status=status.HTTP_409_CONFLICT)

        else:
            return Response({"status": "AUTHENTICATION_FAILED"}, status=status.HTTP_403_FORBIDDEN)
