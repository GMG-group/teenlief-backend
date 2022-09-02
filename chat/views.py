import hashlib

from django.db.models import Q
from django.shortcuts import render

from accounts.models import User
from chat.models import ChatRoom

from teenlief import settings


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    teen_id = room_name.split('l')[0]
    helper_id = room_name.split('l')[1]

    print(teen_id, helper_id)

    chattings = []
    if request.user.id == int(teen_id) or request.user.id == int(helper_id):
        hashed_room_name = hashlib.sha256((teen_id + getattr(settings, 'SECRET_KEY') + helper_id).encode()).hexdigest()

        if not (ChatRoom.objects.filter(Q(user1_id=teen_id) & Q(user2_id=helper_id)).exists() or ChatRoom.objects.filter(Q(user1_id=helper_id) & Q(user2_id=teen_id)).exists()):
            # 채팅방 생성
            ChatRoom.objects.create(room_name=hashed_room_name, user1=User.objects.get(id=teen_id), user2=User.objects.get(id=helper_id))

        else:
            # 기존 로그 리턴 및 채팅방 입장
            chattings = ChatRoom.objects.get(room_name=hashed_room_name).chatlog_set.all()
            print(chattings)

        return render(request, 'chat/room.html', {
            'room_name': hashed_room_name,
            'chattings': chattings,
        })