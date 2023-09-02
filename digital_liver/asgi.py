"""
ASGI config for digital_liver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import include, re_path

import apps.material.urls as maaterial_urls


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digital_liver.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': URLRouter([
        re_path(r'^api/ws/material/', URLRouter(maaterial_urls.websocket_urlpatterns)),
    ]),
})
