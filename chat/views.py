import hashlib

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from accounts.models import User
from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer, ChatLogSerializer

from teenlief.settings import get_env_variable


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    teen_id = room_name.split('l')[0]
    helper_id = room_name.split('l')[1]

    print(teen_id, helper_id)

    chattings = []
    if request.user.id == int(teen_id) or request.user.id == int(helper_id):
        hashed_room_name = hashlib.sha256((teen_id + get_env_variable('SECRET_KEY') + helper_id).encode()).hexdigest()

        if not (ChatRoom.objects.filter(Q(teen_id=teen_id) & Q(helper_id=helper_id)).exists() or ChatRoom.objects.filter(Q(helper_id=helper_id) & Q(teen_id=teen_id)).exists()):
            # 채팅방 생성
            ChatRoom.objects.create(room_name=hashed_room_name, teen=User.objects.get(id=teen_id), helper=User.objects.get(id=helper_id))

        else:
            # 기존 로그 리턴 및 채팅방 입장
            chattings = get_object_or_404(ChatRoom, room_name=hashed_room_name).chatlog_set.all()
            print(chattings)

        return render(request, 'chat/room.html', {
            'room_name': hashed_room_name,
            'chattings': chattings,
        })


class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(teen=self.request.user) | Q(helper=self.request.user))

    def retrieve(self, request, pk=None):
        room = get_object_or_404(ChatRoom, id=pk)
        chatlog = room.chatlog_set.all()
        serializer = ChatLogSerializer(chatlog, many=True)

        return Response(serializer.data)

