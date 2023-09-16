import json
import logging
import threading
import time

from urllib.parse import parse_qs

from apps.material.models import Character
from services import gpt
from services.douyin import DouyinLiveHandler
from utils.auth import get_user
from utils.consumers import CustomJsonWebsocketConsumer
# from utils.userauth import is_usage_limit_reached


class LiveStreamWsConsumer(CustomJsonWebsocketConsumer):
    def connect(self):
        self.closed = False
        self.authenticated = False
        self.live_handler = None
        self.user = None

        # user = self.scope['user']
        # if not user.is_authenticated:
        #     self.close()
        #     return
        # if is_usage_limit_reached(user):
        #     self.close()
        #     return
        
        path_params = self.scope['url_route']['kwargs']
        query_params = parse_qs(self.scope['query_string'].decode(encoding='utf-8'))

        if 'platform' not in path_params \
            or 'room_id' not in path_params \
            or 'character_id' not in query_params:
            logging.warning('Bad request to LiveStreamWsConsumer. Closing...')
            self.close()
            return
        
        self.accept()
        logging.info('LiveStreamWsConsumer connection opened')

        self.platform = path_params['platform']
        self.room_id = path_params['room_id']
        self.character_id = int(query_params['character_id'][0])

        # self.last_ping_time = time.time()
        threading.Thread(target=self._monitor, daemon=True).start()
    
    def disconnect(self, code):
        logging.info(f'LiveStreamWsConsumer disconnected with code: {code}')
        self.closed = True
        if self.live_handler:
            self.live_handler.close()

    def receive_json(self, content):
        if content.get('type') == 'AUTH':
            logging.info('Received auth message for LiveStreamWsConsumer')
            self.user = get_user(content['token'])
            if not self.user.is_authenticated:
                logging.warning(f'User authentication failed for LiveStreamWsConsumer')
                self.close()
                return
            self.authenticated = True
            self._init_handler()
        elif content.get('type') == 'PING':
            logging.info('Received ping message from LiveStreamWsConsumer client')
            # self.last_ping_time = time.time()

            # Send pong message to avoid connection being closed by nginx when idle for 60s
            # See http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_read_timeout
            # self.send(text_data=json.dumps({ 'type': 'PONG' }, ensure_ascii=False))
        else:
            logging.warning(f'Unrecognized message type: {content.get("type")}')

    def _init_handler(self):
        try:
            character = Character.objects.get(id=self.character_id, user_id=self.user.id)
            if self.platform == 'douyin':
                self.live_handler = DouyinLiveHandler(self, character)
                self.live_handler.start_danmu_handler(self.room_id)
            else:
                logging.warning(f'Unsupported livestream platform: {self.platform}')
                self.close()
        except Exception:
            logging.error('Failed to start live stream handler', exc_info=True)
            self.close()

    def _monitor(self):
        for _ in range(5):
            if self.authenticated:
                return
            time.sleep(1)
        
        if not self.authenticated:
            self.close()
            logging.info(f'LiveStreamWsConsumer client was not authenticated in 5 seconds. Closing...')

    # TODO: probably not needed especially when nginx is used (proxy_read_timeout)
    #       Also, the connection will be closed if the browser tab/window is closed
    # def _monitor_ping(self):
    #     while True:
    #         if self.closed:
    #             break
    #         if (time.time() - self.last_ping_time >= 40):
    #             # TODO: Cleanup
    #             # self.live_handler.close()
    #             # self.message_handler.stop_requested = True
    #             logging.info(f'No ping message in the last 30 seconds. Closing the WS connection...')
    #             self.close()
    #             break
    #         time.sleep(5)
