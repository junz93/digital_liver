import json
import logging
import random
import threading
import time

from apps.material.models import Character
from services import gpt, sqlite_conn
from services.gol import Gol
from utils import danmu
from utils.consumers import CustomJsonWebsocketConsumer
from utils.types.enums import MessageEnum, PriorityMessage


message_path = './conf/message_describe.json'
with open(message_path, 'r', encoding='utf-8') as f:
    message_describe = json.load(f)


class MessageHandler:
    def __init__(self, consumer: CustomJsonWebsocketConsumer, gol: Gol, character: Character):
        self.consumer = consumer
        self.gol = gol
        self.character = character
        self.closed = False

        t = threading.Thread(target=self.handle_message, daemon=True)
        t.start()

    def close(self):
        self.closed = True
    
    def _handle_danmu(self, message_priority, chat_message):
        logging.info(f"\t处理弹幕中： {message_priority} -- {chat_message.user.nickName}: {chat_message.content}，线程id：{threading.get_ident()}，各优先级消息还剩余：{self.gol.get_all_list_num()}")

        # 过滤弹幕\昵称中的表情
        chat_message.content = danmu.filer_biaoqing(chat_message.content)
        chat_message.content = danmu.filter_emoji(chat_message.content)
        # 用户名称过滤
        chat_message.user.nickName = danmu.filer_biaoqing(chat_message.user.nickName)
        chat_message.user.nickName = danmu.filter_emoji(chat_message.user.nickName)
        chat_message.user.nickName = danmu.filer_nickname(chat_message.user.nickName)

        answer = ''
        if chat_message.content:
            for segment in gpt.get_answer(chat_message.content, chat_message.user.id, chat_message.eventTime, character=self.character):
                if segment.startswith('抱歉'):
                    logging.warning('弹幕回答以“抱歉”开头，跳过')
                    return
                answer += segment

        if answer and not answer.startswith('生成Gpt回答出错'):
            json_data = {
                'type': 'DANMU',
                'time': chat_message.eventTime,
                'userNickName': chat_message.user.nickName,
                'content': chat_message.content,
                'reply': answer,
            }
            self.consumer.send_json(json_data)
            # logging.debug(f'Sent message to WS client: {json.dumps(json_data, ensure_ascii=False)}')

            user_priority = self.gol.get_user_priority(chat_message.common.roomId, chat_message.user)
            if user_priority <= 5 or user_priority == 7:
                sqlite_conn.db.insert_history_danmu(chat_message, answer)
    
    def _handle_gift(self, message_priority, gift_message):
        try:
            logging.info(f"\t处理礼物中：{gift_message.common.describe}，线程id：{threading.get_ident()}，各优先级消息还剩余：{self.gol.get_all_list_num()}")
            user_name = gift_message.user.nickName
            gift_name = "{}个".format(gift_message.totalCount if gift_message.totalCount else "1") + gift_message.gift.describe.strip("送出")

            if message_priority == PriorityMessage.GiftVip.value:
                gift_template = random.choice(message_describe['vip_gift'])
            elif message_priority == PriorityMessage.GiftExpensive.value:
                gift_template = random.choice(message_describe['expensive_gift'])
            elif message_priority == PriorityMessage.GiftMiddle.value:
                gift_template = random.choice(message_describe['middle_gift'])
            elif message_priority == PriorityMessage.GiftSmall.value:
                gift_template = random.choice(message_describe['small_gift'])
            else:
                logging.warning('当前礼物优先级不存在')
                return

            gift_reply = gift_template.format(user_name=user_name, gift_name=gift_name)

            gift_time = int(str(gift_message.sendTime)[:10])  # 异常：保留前10位
            json_data = {
                'type': 'GIFT',
                'time': gift_time if gift_time else int(time.time()),
                'userNickName': user_name,
                'giftName': gift_message.gift.name,
                'count': gift_message.comboCount,
                'unitPrice': gift_message.gift.diamondCount * 10,  # Unit of price: cent
                'reply': gift_reply,
            }
            self.consumer.send_json(json_data)
            # logging.debug(f'Sent message to WS client: {json.dumps(json_data, ensure_ascii=False)}')
        except Exception:
            logging.exception('生成礼物回复出错')

    def _handle_enter(self, message_priority, member_message):
        try:
            room_id = member_message.common.roomId
            user_priority = self.gol.get_user_priority(room_id, member_message.user)
            enter_message = random.choice(message_describe[f'enter_level{user_priority}'])

            logging.info(f"\t处理进入直播间观众消息中，用户名：{member_message.user.nickName}, 等级:{user_priority}，线程id：{threading.get_ident()}，各优先级消息还剩余：{self.gol.get_all_list_num()}")

            member_message.user.nickName = danmu.filer_nickname(member_message.user.nickName)
            enter_describe = enter_message.format(user_name=member_message.user.nickName)

            json_data = {
                'type': 'ENTER',
                # 'time': member_message.common.createTime,
                'time': int(time.time()),
                'userNickName': member_message.user.nickName,
                # 'userLevel': danmu.get_user_level(member_message.user),
                # 'allTimeAmount': self.gol.get_history_user_gift(room_id, member_message.user.id) * 10,
                'reply': enter_describe,
            }
            self.consumer.send_json(json_data)
        except Exception:
            logging.exception('生成进入直播间回复出错')

    def _handle_like(self, message_priority, like_message):
        try:
            logging.info(f"\t处理点赞观众消息中，用户名：{like_message.user.nickName}, 线程id：{threading.get_ident()}，各优先级消息还剩余：{self.gol.get_all_list_num()}")
            user_name = danmu.filter_emoji(like_message.user.nickName)
            user_name = danmu.filer_biaoqing(user_name)
            user_name = danmu.filer_nickname(user_name)
            like_describe = random.choice(message_describe["like_describe"]).format(user_name=user_name)

            json_data = {
                'type': 'LIKE',
                'time': int(time.time()),
                'userNickName': user_name,
                'reply': like_describe,
            }
            self.consumer.send_json(json_data)
        except Exception:
            logging.exception('生成点赞回复出错')



    def _handle_insert(self, message_priority, insert_message):
        try:
            if insert_message:
                logging.info(f"\t处理插队点赞观众消息中，用户名：{insert_message.user.nickName}, 线程id：{threading.get_ident()}，各优先级消息还剩余：{self.gol.get_all_list_num()}")
                user_name = danmu.filter_emoji(insert_message.user.nickName)
                user_name = danmu.filer_biaoqing(user_name)
                user_name = danmu.filer_nickname(user_name)
                like_describe = random.choice(message_describe["like_describe"]).format(user_name=user_name)

                json_data = {
                    'type': 'LIKE',
                    'time': int(time.time()),
                    'userNickName': user_name,
                    'reply': like_describe,
                }
                self.consumer.send_json(json_data)

            logging.info(f"\t生成插队求互动消息中")
            ask_message = random.choice(message_describe["ask_like"] + message_describe["ask_gift"] + message_describe["ask_interaction"])
            
            json_data = {
                'type': 'ASK',
                'time': int(time.time()),
                'reply': ask_message,
            }
            self.consumer.send_json(json_data)
        except Exception:
            logging.exception('生成插队点赞回复出错')

    def handle_message(self):
        # time.sleep(10)  # 等待gol.init初始化
        while True:
            try:
                if self.closed:
                    break

                message_priority, message_type, message = self.gol.get_message()
                if message_type is None:
                    pass
                elif message_type == MessageEnum.InsertMessage:
                    # self._handle_insert(message_priority, message)
                    pass
                elif message_type == MessageEnum.GiftMessage:
                    self._handle_gift(message_priority, message)
                elif message_type == MessageEnum.ChatMessage:
                    self._handle_danmu(message_priority, message)
                elif message_type == MessageEnum.EnterMessage:
                    self._handle_enter(message_priority, message)
                elif message_type == MessageEnum.LikeMessage:
                    self._handle_like(message_priority, message)
                time.sleep(0.5)
            except Exception:
                logging.exception(f'Failed to handle message: {message}')


# def reload_embedding():
#     while True:
#         try:
#             now = datetime.datetime.now()
#             embedding_file = f"../data/embedding/embedding.pickle"
#             realtime_file = f"../resource/实时信息.txt"
#             # 不存在embedding文件或者实时信息文件的写入日期小于今天
#             if not os.path.exists(embedding_file) or not os.path.exists(
#                     realtime_file) or datetime.datetime.fromtimestamp(os.path.getmtime(realtime_file)).strftime(
#                     "%Y-%m-%d") < now.strftime("%Y-%m-%d"):
#                 gpt.init_embedding()
#             time.sleep(5)
#         except Exception as e:
#             logging.exception(f"reload embedding Threading Exception: {e}")
