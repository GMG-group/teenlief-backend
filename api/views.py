from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from accounts.models import User
from api.models import Marker, Promise, Tag, Shelter
from api.serializers import MarkerSerializer, PromiseSerializer, MarkerSimpleSerializer, TagSerializer, \
    ShelterSerializer


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def perform_create(self, serializer):
        serializer.save(helper=self.request.user)


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
