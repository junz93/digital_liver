from channels.generic.websocket import JsonWebsocketConsumer

import json


class CustomJsonWebsocketConsumer(JsonWebsocketConsumer):
    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False)
