import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        print(self.room_name)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


# {
#     'groups': [],
#     'scope': {
#          'type': 'websocket',
#          'path': '/ws/chat/test/',
#          'raw_path': b'/ws/chat/test/',
#          'headers': [
#              (b'host', b'127.0.0.1:8001'),
#              (b'connection', b'Upgrade'),
#              (b'pragma', b'no-cache'),
#              (b'cache-control', b'no-cache'),
#              (b'user-agent', b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'),
#              (b'upgrade', b'websocket'), (b'origin', b'http://127.0.0.1:8001'),
#              (b'sec-websocket-version', b'13'),
#              (b'accept-encoding', b'gzip, deflate, br'),
#              (b'accept-language', b'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6,ja;q=0.5'),
#              (b'cookie', b'tabstyle=html-tab; nossu-refresh-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MjAzNjc0OSwiaWF0IjoxNjYxNDMxOTQ5LCJqdGkiOiJhMjUwZTc3MzI5ZjU0MzdhOTZkNjlhYWJkYmI2MzI5YiIsInVzZXJfaWQiOjEwfQ.vaZdpHnLTROSOuxBqgdkA-KX4PDtHXF3ND_4XGWe1Mo; ch-veil-id=64282ff3-8530-4c2e-940a-0b14feb15053; accountId=37; messages=.eJwliUEKgCAURK8SrkXKFF12DxXRnwWBGan3z0-bmXlvjCHeX7XcPqdaw5kInSmXlDzv4LK1VBuDkifbQa1ge9QSpr9sD_uh8VAalVgQJGDyKIfhuCNPghHnPp_1I0s:1oTQ26:rYMaY4JvKJhWuHcjpFom9TiBySZPW2hKM-f5yMNtqSs; sessionid=kopxymao7kkafy2pzshsg3ivlag17xk0; teenlief-auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxOTY4NDQ4LCJpYXQiOjE2NjE5NjEyNDgsImp0aSI6ImJlNTI0MDQzMGNmMDRkMjk5OTliMTY2YzM2MmM1ZTZiIiwidXNlcl9pZCI6MTh9.WZom6c6seI18ve1c-E-WlGRBzAF4JF9WOEgf9OqV6G8; teenlief-refresh-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MjU2NjA0OCwiaWF0IjoxNjYxOTYxMjQ4LCJqdGkiOiJhMjRiZGI3NjgxYzE0NTgwYWNhZjMxYTdjZmVmYWQ4NCIsInVzZXJfaWQiOjE4fQ.HjxDkpZroPIFWR8o5Q9r9xOjeq_TICxHOh9P_8QXpIY; csrftoken=FHLnTagiuq5HIFH8sPpi18c5wZjxDL5BlbDtG08vXoRWMtsUiCM2wQ9GaS0mGNXg'),
#              (b'sec-websocket-key', b'+bkP/elCbJlI/ktyfZH8UA=='),
#              (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')
#          ],
#     'query_string': b'',
#     'client': ['127.0.0.1', 58171],
#     'server': ['127.0.0.1', 8001],
#     'subprotocols': [],
#     'asgi': {'version': '3.0'},
#     'cookies': {
#      'tabstyle': 'html-tab',
#      'nossu-refresh-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MjAzNjc0OSwiaWF0IjoxNjYxNDMxOTQ5LCJqdGkiOiJhMjUwZTc3MzI5ZjU0MzdhOTZkNjlhYWJkYmI2MzI5YiIsInVzZXJfaWQiOjEwfQ.vaZdpHnLTROSOuxBqgdkA-KX4PDtHXF3ND_4XGWe1Mo',
#      'ch-veil-id': '64282ff3-8530-4c2e-940a-0b14feb15053',
#      'accountId': '37',
#      'messages': '.eJwliUEKgCAURK8SrkXKFF12DxXRnwWBGan3z0-bmXlvjCHeX7XcPqdaw5kInSmXlDzv4LK1VBuDkifbQa1ge9QSpr9sD_uh8VAalVgQJGDyKIfhuCNPghHnPp_1I0s:1oTQ26:rYMaY4JvKJhWuHcjpFom9TiBySZPW2hKM-f5yMNtqSs',
#      'sessionid': 'kopxymao7kkafy2pzshsg3ivlag17xk0',
#      'teenlief-auth': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxOTY4NDQ4LCJpYXQiOjE2NjE5NjEyNDgsImp0aSI6ImJlNTI0MDQzMGNmMDRkMjk5OTliMTY2YzM2MmM1ZTZiIiwidXNlcl9pZCI6MTh9.WZom6c6seI18ve1c-E-WlGRBzAF4JF9WOEgf9OqV6G8',
#      'teenlief-refresh-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MjU2NjA0OCwiaWF0IjoxNjYxOTYxMjQ4LCJqdGkiOiJhMjRiZGI3NjgxYzE0NTgwYWNhZjMxYTdjZmVmYWQ4NCIsInVzZXJfaWQiOjE4fQ.HjxDkpZroPIFWR8o5Q9r9xOjeq_TICxHOh9P_8QXpIY',
#      'csrftoken': 'FHLnTagiuq5HIFH8sPpi18c5wZjxDL5BlbDtG08vXoRWMtsUiCM2wQ9GaS0mGNXg'
#     },
#     'session': <django.utils.functional.LazyObject object at 0x7f96f8c19970>,
#     'user': <channels.auth.UserLazyObject object at 0x7f96f8c19fa0>,
#     'path_remaining': '',
#     'url_route': {'args': (), 'kwargs': {'room_name': 'test'}}},
#     'channel_layer': <channels_redis.core.RedisChannelLayer object at 0x7f96e8b8c4c0>,
#     'channel_name': 'specific.cb356756a583448b86652883fec278ff!af38f1e19c164af986facc75623b5f0a',
#     'channel_receive': functools.partial(<bound method RedisChannelLayer.receive of <channels_redis.core.RedisChannelLayer object at 0x7f96e8b8c4c0>>,
#     'specific.cb356756a583448b86652883fec278ff!af38f1e19c164af986facc75623b5f0a'),
#     'base_send': <bound method InstanceSessionWrapper.send of <channels.sessions.InstanceSessionWrapper object at 0x7f96e8b8c550>>,
#     'room_name': 'test',
#     'room_group_name': 'chat_test'
# }
