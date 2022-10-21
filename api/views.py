from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from api.models import Marker, Promise, Tag, Shelter
from api.serializers import MarkerSerializer, PromiseSerializer, MarkerSimpleSerializer, TagSerializer, \
    ShelterSerializer, MyMarkerSerializer


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

        serializer = serializer_class(queryset, many=True, context={'request': request}) # context 안붙이면 full url로 안나옴 https://stackoverflow.com/a/69900733
        return Response(serializer.data)


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer


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
