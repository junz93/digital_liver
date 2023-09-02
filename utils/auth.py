from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import TokenAuthentication


token_auth = TokenAuthentication()


def get_user(token_str: str):
    try:
        user, token = token_auth.authenticate_credentials(token_str)
    except:
        user = AnonymousUser()
    
    return user


@database_sync_to_async
def get_user_async(token_str: str):
    return get_user(token_str)


class TokenAuthMiddleware:
    """
    Custom middleware for token-based (per-request) authentication.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app
    
    async def __call__(self, scope, receive, send):
        headers = scope['headers']
        auth_header = headers.get('Authorization', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'Token':
            user = AnonymousUser()
        else:
            user = await get_user_async(auth_header[1])
        scope['user'] = user

        return await self.app(scope, receive, send)
