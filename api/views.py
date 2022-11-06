from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
# from teenlief-backend.api.serializers import ReviewSerializer
from rest_framework.generics import get_object_or_404

from accounts.models import User
from accounts.serializers import UserSerializer
from api.models import Marker, Promise, Tag, Shelter, Review, PointLog, HelperInfo
from api.serializers import MarkerSerializer, PromiseSerializer, MarkerSimpleSerializer, TagSerializer, \
    ReviewSerializer, \
    ShelterSerializer, PointSerializer, MyMarkerSerializer, HelperInfoSerializer

from django.shortcuts import get_object_or_404

from rest_framework.decorators import action


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def perform_create(self, serializer):
        serializer.save(helper=self.request.user)

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

        serializer = self.serializer_class(queryset, many=True, context={'request': request})  # context 안붙이면 full url로 안나옴 https://stackoverflow.com/a/69900733
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

    def retrieve(self, request, pk=None):
        queryset = Review.objects.filter(helper_id=pk)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)


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

        serializer = self.serializer_class(queryset, many=True, context={'request': request})  # context 안붙이면 full url로 안나옴 https://stackoverflow.com/a/69900733
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
        user = request.user
        user.certificated = True
        user.save()
        res = UserSerializer(user)
        return Response(res.data)
