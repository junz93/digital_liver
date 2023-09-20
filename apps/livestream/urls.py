from django.urls import path, re_path

from . import consumers
# from . import views


urlpatterns = [
]

websocket_urlpatterns = [
    re_path(r'main/(?P<platform>\w+)/(?P<room_id>\w+)$', consumers.LiveStreamWsConsumer.as_asgi()),
]
