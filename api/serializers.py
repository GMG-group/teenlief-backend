from rest_framework import serializers
from .models import Marker, Promise, Tag


class PromiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promise
        fields = '__all__'


class MarkerSerializer(serializers.ModelSerializer):
    promises = PromiseSerializer(read_only=True, many=True)

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
        fields = ('latitude', 'longitude')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
