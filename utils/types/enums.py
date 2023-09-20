from enum import IntEnum


# 消息类型
class MessageEnum(IntEnum):
    GiftMessage = 0
    ChatMessage = 1
    EnterMessage = 2
    LikeMessage = 3
    InsertMessage = 9  # 插队消息


# 消息优先级
# 修改优先级需要配合gol.message_list中的顺序
class PriorityMessage(IntEnum):
    InsertPriority = 0  # 插队消息优先级
    GiftVip = 1
    GiftExpensive = 2
    DanmuVip = 3
    EnterHighLevel = 4
    GiftMiddle = 5
    DanmuExpensive = 6
    DanmuMiddle = 7
    GiftSmall = 8
    DanmuHighLevel = 9
    Danmu = 10
    Like = 11


# 视频号礼物类型
ShiPinHaoGift = {
    "爱心": 1,
    "解暑西瓜": 1,
    "棒棒糖": 3,
    "干杯": 10,
    "咖啡": 20,
    "么么哒": 6,
    "草莓蛋糕": 30,
    "桃花岛": 30000,
    "荣耀之心": 520,
    "我来了": 100,
    "超好看": 5,
    "墨镜": 99,
    "拜拜": 100,
    "奶茶": 166,
    "撸串": 50,
    "狮子座": 666,
    "小飞机": 610,
    "兔飞猛进": 999,
    "告白气球": 520,
    "真好听": 5,
    "彩虹车": 3000,
    "火箭": 2000,
    "巧克力": 388,
    "抱抱": 299,
    "摸摸头": 166,
    "晚安": 100,
    "甜蜜告白": 188,
    "锦鲤": 799,
    "动物观光": 500,
    "口红": 200,
    "一生一世": 1314,
    "摘星星": 5000,
    "梦幻城堡": 10000,
    "游乐园": 20000,
    "一箭钟情": 15000,
    "粉丝牌": 1,
    "加油": 6,
    "比心": 188,
    "情书": 498,
    "守护": 1314,
    "为你加冕": 5200,
    "超级跑车": 1888,
    "海景别墅": 3888,
    "豪华游艇": 8888,
    "私人飞机": 13140,
    "繁华都市": 18888,
    "星际飞船": 20000,
    "人气宝": 299,
    "真爱召唤": 999,
    "人气传送": 9999,
}