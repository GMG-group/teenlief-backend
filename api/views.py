from rest_framework import viewsets
from api.models import Marker, Promise
from api.serializers import MarkerSerializer, PromiseSerializer


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
