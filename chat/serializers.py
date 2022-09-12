from rest_framework import serializers
from .models import ChatRoom, ChatLog


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
        depth = 2


class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        fields = '__all__'
        depth = 2
