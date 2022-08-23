from rest_framework import serializers
from .models import Marker, Promise


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
