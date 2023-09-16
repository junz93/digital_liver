import logging
import threading
import time

# from asgiref.sync import sync_to_async
# from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from .models import Character
from services import gpt
from utils.auth import get_user
from utils.consumers import CustomJsonWebsocketConsumer


class AiGeneratorWsConsumer(CustomJsonWebsocketConsumer):
    def connect(self):
        self.closed = False
        self.generating = False
        
        # logging.info(f'Websocket scope: {self.scope}')
        
        path_params = self.scope['url_route']['kwargs']
        query_params = parse_qs(self.scope['query_string'].decode(encoding='utf-8'))
        self.mode = path_params['mode'].upper()
        
        if 'character_id' not in query_params \
            or 'query' not in query_params \
            or (self.mode != gpt.AnswerMode.CHAT and self.mode != gpt.AnswerMode.SPEECH):
            self.close()
            return
        
        self.accept()
        logging.info('AiGeneratorWsConsumer connection opened')
        
        self.character_id = int(query_params['character_id'][0])
        self.query = query_params['query'][0]
        
        threading.Thread(target=self._monitor, daemon=True).start()
    
    def disconnect(self, code):
        logging.info(f'AiGeneratorWsConsumer disconnected with code: {code}')
        self.closed = True

    def receive_json(self, content):
        if self.generating:
            return
        self.generating = True
        
        try:
            if content.get('type') == 'AUTH':
                logging.info('Received auth message for AiGeneratorWsConsumer')
                
                user = get_user(content['token'])
                if not user.is_authenticated:
                    logging.warning(f'User authentication failed for AiGeneratorWsConsumer')
                    return
                
                try:
                    character = Character.objects.get(id=self.character_id, user_id=user.id)
                    i = 0
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
                        if self.closed:
                            break
                        self.send_json({'type': 'CONTENT_SEGMENT', 'seq_no': i, 'data': segment})
                        i += 1
                        time.sleep(0.1)
                except Character.DoesNotExist:
                    logging.warning(f'Cannot find a character with ID {self.character_id}')
                except Exception as e:
                    logging.exception('An error happened while generating content')
            else:
                logging.warning(f'Unrecognized message type: {content.get("type")}')
        finally:
            self.close()
    
    def _monitor(self):
        for _ in range(5):
            if self.generating:
                return
            time.sleep(1)
        
        if not self.generating:
            self.close()
            logging.info(f'No client message in 5 seconds. Closing...')
