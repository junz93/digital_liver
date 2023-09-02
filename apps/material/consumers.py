import asyncio
import json
import logging
# import threading
import time

# from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
# from channels.generic.http import AsyncHttpConsumer
from channels.generic.websocket import JsonWebsocketConsumer
from urllib.parse import parse_qs

from .models import Character
from services import gpt
from utils.auth import get_user


class CustomJsonWebsocketConsumer(JsonWebsocketConsumer):
    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, ensure_ascii=False)


class AiGeneratorWsConsumer(CustomJsonWebsocketConsumer):
    def connect(self):
        self.closed = False
        self.authenticated = False
        
        logging.info(f'Websocket scope: {self.scope}')

        self.accept()
        logging.info('Websocket connection opened')
        
        path_params = self.scope['url_route']['kwargs']
        query_params = parse_qs(self.scope['query_string'].decode(encoding='utf-8'))
        self.character_id = int(path_params['character_id'])
        self.mode = path_params['mode'].upper()

        if 'query' not in query_params \
            or (self.mode != gpt.AnswerMode.CHAT and self.mode != gpt.AnswerMode.SCRIPT):
            self.close()
            return
        
        self.query = query_params['query'][0]
    
    def disconnect(self, code):
        logging.info(f'Websocket disconnected with code: {code}')
        self.closed = True

    def receive_json(self, content):
        try:
            if content.get('type') == 'AUTH':
                logging.info('Received auth message for websocket')
                
                user = get_user(content['token'])
                if not user.is_authenticated:
                    logging.warning(f'User authentication failed')
                    return
                
                self.authenticated = True
                try:
                    character = Character.objects.get(id=self.character_id, user_id=user.id)
                    for segment in gpt.get_answer(
                        self.query, 
                        f'user_{user.id}' if self.mode == gpt.AnswerMode.CHAT else None, 
                        int(time.time()), 
                        with_censorship=False, 
                        character=character, 
                        mode=self.mode
                    ):
                        # if segment.startswith('生成Gpt回答出错'):
                        #     return
                        self.send_json({'data': segment})
                        time.sleep(0.1)
                except Character.DoesNotExist:
                    logging.warning(f'Cannot find a character with ID {self.character_id}')
                except Exception as e:
                    logging.exception('An error happened while generating content')
            else:
                logging.warning(f'Unrecognized message type: {content.get("type")}')
        finally:
            self.close()


# class AiGeneratorConsumer(AsyncHttpConsumer):
#     async def handle(self, body):
#         await self.send_headers(headers=[
#             (b'Cache-Control', b'no-cache'),
#             (b'Content-Type', b'text/event-stream; charset=utf-8'),
#             # (b'Transfer-Encoding', b'chunked'),
#         ])

#         user = self.scope['user']
#         if not user.is_authenticated:
#             await self.close(403, 'Not logged in')
#             return

#         # if await database_sync_to_async(is_usage_limit_reached)(user):
#         #     await self.close(403, 'Max usage time was reached')
#         #     return

#         path_params = self.scope['url_route']['kwargs']
#         query_params = parse_qs(self.scope['query_string'].decode(encoding='utf-8'))
#         mode = path_params['mode'].upper()

#         if 'character_id' not in path_params \
#             or 'query' not in query_params \
#             or (mode != gpt.AnswerMode.CHAT and mode != gpt.AnswerMode.SCRIPT):
#             await self.close(400, 'Invalid input')
#             return
        
#         character_id = int(path_params['character_id'])
#         query = query_params['query'][0]

#         try:
#             character = await self.get_character(character_id, user.id)
#             # for segment in await sync_to_async(gpt.get_answer)(
#             for segment in gpt.get_answer(
#                 query, 
#                 f'user_{user.id}' if mode == gpt.AnswerMode.CHAT else None, 
#                 int(time.time()), 
#                 with_censorship=False, 
#                 character=character, 
#                 mode=mode
#             ):
#                 if segment.startswith('生成Gpt回答出错'):
#                     await self.close(500, 'Failed to generate content')
#                     return
                
#                 # logging.info('Received a segment')
#                 await self.send_message(segment)
#                 await asyncio.sleep(0.1)
            
#             await self.close(200, 'Completed successfully')
#         except Character.DoesNotExist:
#             await self.close(404, f'Cannot find a character with ID {character_id}')
#         except Exception as e:
#             logging.exception('An error happened while generating content')
#             await self.close(500, 'An error happened while generating content')

#     @database_sync_to_async
#     def get_character(self, character_id: int, user_id: int):
#         return Character.objects.get(id=character_id, user_id=user_id)

#     async def send_message(
#         self, 
#         data, 
#         code: int = None, 
#         message: str = None, 
#         is_last = False
#     ):
#         json_data = { 'data': data }
#         if code is not None:
#             json_data['code'] = code
#         if message is not None:
#             json_data['message'] = message

#         data = json.dumps(json_data, ensure_ascii=False)

#         body = f'data: {data}\n\n'.encode('utf-8')
#         await self.send_body(body, more_body=(not is_last))
    
#     async def close(self, code: int, message: str):
#         await self.send_message('', code, message, True)
