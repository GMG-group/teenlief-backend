from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken


# @database_sync_to_async
# def get_user(token_key):
#     try:
#         token = Token.objects.get(key=token_key)
#         return token.user
#     except Token.DoesNotExist:
#         return AnonymousUser()

@database_sync_to_async
def get_user(access_token_str):
    access_token_obj = AccessToken(access_token_str)
    user_id = access_token_obj['user_id']
    from accounts.models import User
    user = User.objects.get(id=user_id)

    return user


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
