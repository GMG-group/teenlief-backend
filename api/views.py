from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
# from teenlief-backend.api.serializers import ReviewSerializer

from accounts.models import User
from api.models import Marker, Promise, Tag, Shelter, Review
from api.serializers import MarkerSerializer, PromiseSerializer, MarkerSimpleSerializer, TagSerializer, ReviewSerializer, \
    ShelterSerializer

from django.http import HttpResponse

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


class CheckUserMarkerExistsAPI(APIView):
    def get(self, request, user_id):
        marker = Marker.objects.filter(helper_id=user_id)
        if marker.exists():
            return Response(marker[0].id)
        else:
            return Response(False)

class MarkerReviewListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        print("??????????????????????????????????????????????????????", queryset)
        # serializer = ReviewSerializer(queryset, many=True)
        # return Response(serializer.data)