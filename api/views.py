from rest_framework import viewsets, status
from rest_framework.response import Response

from accounts.models import User
from api.models import Marker, Promise, Tag
from api.serializers import MarkerSerializer, PromiseSerializer, MarkerSimpleSerializer, TagSerializer


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(helper=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer


class MarkerSimpleViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSimpleSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
