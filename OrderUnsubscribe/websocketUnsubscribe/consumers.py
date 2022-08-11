from cmath import pi
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.http import HttpResponse, JsonResponse 
import time,datetime,random
from django.db.models.functions import Substr 

#从views中导入User信息
from .views import OrderUnsubscribeInfoList
from users.models import OrderUnsubscribeInfo
from users.serializers import OrderUnsubscribeInfoModelSerializer
from rest_framework.response import Response

from django.db.models import Min,Max,Count,Sum,Avg
from django.db.models.functions import TruncDay, TruncHour, TruncMonth
from django.db import connection
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import  asyncio
#解决：You cannot call this from an async context - use a thread or sync_to_async
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

class AsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):  # 连接时触发
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', 'room_name')
        self.room_group_name = 'notice_%s' % self.room_name  # 直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。

        # 将新的连接加入到群组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        while True:
            cur_time = time.strftime('%X',time.localtime(time.time()))
            cur_time = datetime.time(*map(int, cur_time.split(':')))
            try:
                queryset = OrderUnsubscribeInfo.objects.filter(ActionTime=cur_time).values('UserPseudoCode_x','ActionTime','ProductId_x').distinct()
                # serializer = OrderUnsubscribeInfoModelSerializer(queryset_old, many=True)
                # queryset = OrderUnsubscribeInfo.objects.all().values('ActionTime','url','UserPseudoCode_x')
                # datas_old = json.dumps(serializer.data)
                # datas = json.loads(datas_old)

                for data in queryset:
                    username = data.get('UserPseudoCode_x','')
                    ActionTime = data.get('ActionTime','')
                    ProductId = data.get('ProductId_x','')
                    product_str = ProductId_name.get(ProductId,'移动2022畅游流量包')
                    mobile = get_mobile()
                    strs = f"用户{mobile}在{ActionTime}订购了{product_str},免流中."

                    await self.send(text_data=json.dumps({
                            'message': strs
                        }))
                    #执行self.send()之后必须加这一行才能成功发送数据到前端websocket
                    await asyncio.sleep(3)

            except Exception as e:
                print(e)
                pass

        #按照product_id分类统计个数
        # queryset_old = OrderUnsubscribeInfo.objects.values('ProductId_x').annotate(c=Count('ProductId_x'))
        # 按照时间段分组统计个数，以1小时为单位
        # queryset_old = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-1-1','2022-12-31')).annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        

    async def disconnect(self, close_code):  # 断开时触发
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):  # 接收消息时触发
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 信息群发
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'system_message',
                'message': message
            }
        )

    # Receive message from room group
    async def system_message(self, event):
        print(event)
        message = event['message']

        # Send message to WebSocket单发消息
        await self.send(text_data=json.dumps({
            'message': message
        }))

#异步方式获取数据
@database_sync_to_async
def get_username(username):
    return OrderUnsubscribeInfo.objects.filter(UserPseudoCode_x=username)

def get_mobile():
    mobiles = ['130', '131', '132', '133', '134','156','187','149']
    number  = str(int(time.time()))[2:]
    mobile  = random.choice(mobiles)+number
    return mobile

def pro_dic(queryset):
    """
        累加个数
    """
    dict_lis = []
    if queryset:
        for k,v in dict(queryset).items():
            dic = {"curtime":str(k),"count":v}
            dict_lis.append(dic)
    return dict_lis

def parse_user_OrderUnsubscribeInfo():
    """
    从mysql数据库中获取数据并解析
    """

    #指定具体用户名并获取用户信息
    username = '5B012E6D4CF86E78964C9350192E77E4'
    userinfo_queryset = get_username(username=username)

    serializer = OrderUnsubscribeInfoModelSerializer(userinfo_queryset, many=True)
    datas_old = json.dumps(serializer.data)
    datas = json.loads(datas_old)

    if datas:
        url_lis = []
        lis = []
        for data in datas:
            username = data.get('UserPseudoCode_x','')
            ActionTime = data.get('ActionTime','')
            url = data.get('url','')
            if 'music.163' in url:
                url_lis.append('网易云音乐渠道')
            elif 'kugou' in url:
                url_lis.append('酷狗音乐渠道')
            elif 'kuwo' in url:
                url_lis.append('酷我音乐渠道')
            elif 'qq' in url:
                url_lis.append('QQ音乐渠道')
            elif 'taobao' in url:
                url_lis.append('淘宝商城渠道')
            elif 'iqiyi' in url:
                url_lis.append('爱奇艺渠道')
            elif 'vivo' in url:
                url_lis.append('VIVO渠道')
            elif 'douyu' in url:
                url_lis.append('斗鱼渠道')
            elif 'gitshow' in url:
                url_lis.append('快手渠道')
            elif 'snssdk' in url:
                url_lis.append('今日头条渠道')
            elif 'bilibili' in url:
                url_lis.append('哔哩哔哩渠道')
            elif 'mgtv' in url:
                url_lis.append('芒果TV渠道')
            elif 'ffapi' in url:
                url_lis.append('ffapi渠道')
            elif 'bjk' in url:
                url_lis.append('网易白金星卡渠道')

            ProductId = data.get('ProductId_x','')
            lis.append(ProductId)
        pro_lis = []
        url_str = '+'.join(list(set(url_lis)))
        for i in list(set(lis)):
            pro_lis.append(ProductId_name.get(i,'移动新款铂金卡'))
        product_str = '+'.join(list(pro_lis))
        strs = f"时间：{ActionTime}, 用户：{username}，订购了{product_str}, 可以在{url_str}免流使用"
    return strs

ProductId_name = {
    "500000050078":"移动花卡宝藏版29（月租型）",
    "500000050003":"移动花卡宝藏版2020-19元套卡",
    "100000001271":"随心看会员",
    "100000001125":"随心看会员-首月1元促销包",
    "100000001132":"动感地带5G通行证2020-30元",
    "100000091447":"随心听会员（15GB版）"
}

def parse_realTime_OrderUnsubscribeInfo():
    """
    从mysql数据库中获取数据并解析
    """
    #已登录用户订购过哪些产品

    #从数据库中查询数据集并发送到用户页面
    while True:
        time.sleep(3)
        cur_time = time.strftime('%X',time.localtime(time.time()))
        cur_time = datetime.time(*map(int, cur_time.split(':')))
        try:
            queryset_old = OrderUnsubscribeInfo.objects.filter(ActionTime=cur_time)
            serializer = OrderUnsubscribeInfoModelSerializer(queryset_old, many=True)
            # queryset = OrderUnsubscribeInfo.objects.all().values('ActionTime','url','UserPseudoCode_x')
            datas_old = json.dumps(serializer.data)
            datas = json.loads(datas_old)
            url_lis = []
            lis = []
            for data in datas:
                username = data.get('UserPseudoCode_x','')
                ActionTime = data.get('ActionTime','')
                url = data.get('url','')
                if 'music.163' in url:
                    url_lis.append('网易云音乐渠道')
                elif 'kugou' in url:
                    url_lis.append('酷狗音乐渠道')
                elif 'kuwo' in url:
                    url_lis.append('酷我音乐渠道')
                elif 'qq' in url:
                    url_lis.append('QQ音乐渠道')
                elif 'taobao' in url:
                    url_lis.append('淘宝商城渠道')
                elif 'iqiyi' in url:
                    url_lis.append('爱奇艺渠道')
                elif 'vivo' in url:
                    url_lis.append('VIVO渠道')
                elif 'douyu' in url:
                    url_lis.append('斗鱼渠道')
                elif 'gitshow' in url:
                    url_lis.append('快手渠道')
                elif 'snssdk' in url:
                    url_lis.append('今日头条渠道')
                elif 'bilibili' in url:
                    url_lis.append('哔哩哔哩渠道')
                elif 'mgtv' in url:
                    url_lis.append('芒果TV渠道')
                elif 'ffapi' in url:
                    url_lis.append('ffapi渠道')
                elif 'bjk' in url:
                    url_lis.append('网易白金星卡渠道')

                ProductId = data.get('ProductId_x','')
                lis.append(ProductId)
            pro_lis = []
            url_str = '+'.join(list(set(url_lis)))
            for i in list(set(lis)):
                pro_lis.append(ProductId_name.get(i,'移动新款铂金卡'))
            product_str = '+'.join(list(pro_lis))
            strs = f"时间：{ActionTime}, 用户：{username}，订购了{product_str}, 可以在{url_str}免流使用"

        except Exception as e:
            print(e)
            pass
