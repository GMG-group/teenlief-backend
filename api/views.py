from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# from teenlief-backend.api.serializers import ReviewSerializer
from rest_framework.generics import get_object_or_404

from accounts.models import User
from api.models import Marker, Promise, Tag, Shelter, Review, PointLog
from api.serializers import MarkerSerializer, PromiseSerializer, MarkerSimpleSerializer, TagSerializer, ReviewSerializer, \
    ShelterSerializer, PointSerializer

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


class MarkerReviewListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        print("??????????????????????????????????????????????????????", queryset)
        # serializer = ReviewSerializer(queryset, many=True)
        # return Response(serializer.data)