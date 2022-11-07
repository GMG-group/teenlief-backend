from rest_framework import serializers

from accounts.serializers import UserSerializer
from api.models import Marker, Promise, Tag, Shelter, Review, PointLog, HelperInfo


class PromiseSerializer(serializers.ModelSerializer):
    reviewed = serializers.BooleanField(read_only=True)
    helper = UserSerializer(read_only=True)

    class Meta:
        model = Promise
        fields = '__all__'
        read_only_fields = ['helper']


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
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author']

    def create(self, validated_data):
        print(validated_data)
        review = Review.objects.create(**validated_data)
        helper = validated_data['helper']

        helperInfo = HelperInfo.objects.filter(helper=helper)[0]

        if not helperInfo:
            helperInfo = HelperInfo.objects.create(helper=helper, review_count=0, score=0, total=0)

        helperInfo.review_count += 1
        helperInfo.total += validated_data['stars']
        helperInfo.score = helperInfo.total / helperInfo.review_count
        helperInfo.save()

        promise = validated_data['promise']
        promise.reviewed = True
        promise.save()

        return review


class MyMarkerSerializer(serializers.ModelSerializer):
    promise_count = serializers.SerializerMethodField('get_promise_count')

    class Meta:
        model = Marker
        fields = '__all__'

    def get_promise_count(self, marker):
        return marker.promises.all().count()



class HelperInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelperInfo
        fields = ('id', 'score', 'review_count')