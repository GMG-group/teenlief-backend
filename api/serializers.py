from rest_framework import serializers

from accounts.serializers import UserSerializer
from api.models import Marker, Promise, Tag, Shelter, Review, PointLog


class PromiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promise
        fields = '__all__'


class MarkerSerializer(serializers.ModelSerializer):
    promises = PromiseSerializer(read_only=True, many=True)
    helper = UserSerializer(read_only=True)

    class Meta:
        model = Marker
        fields = '__all__'
        read_only_fields = ['helper']

    def create(self, validated_data):
        tags = validated_data.pop('tag')
        marker = Marker.objects.create(**validated_data)

        for tag in tags:
            marker.tag.add(tag)
        return marker


class MarkerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = ('id', 'latitude', 'longitude', 'tag')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointLog
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MyMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = '__all__'
