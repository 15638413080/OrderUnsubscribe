from cgi import print_arguments
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.response import Response
import json
from django.db.models.functions import TruncDay, TruncHour, TruncMonth, TruncWeek, TruncMonth
from django.db.models import Min,Max,Count,Sum,Avg
import time, datetime
import pandas as pd


#从users应用中导入model
from users.models import OrderUnsubscribeInfo
from users.serializers import OrderUnsubscribeInfoModelSerializer


ProductId_name = {
    "500000050078":"移动花卡宝藏版29（月租型）",
    "500000050003":"移动花卡宝藏版2020-19元套卡",
    "100000001271":"随心看会员",
    "100000001125":"随心看会员-首月1元促销包",
    "100000001132":"动感地带5G通行证2020-30元",
    "100000091447":"随心听会员（15GB版）"
}

import socket
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def last_time():
    now_time=datetime.datetime.now()        
    dt1=now_time+datetime.timedelta(days=-1)
    ds1 = dt1.strftime("%Y-%m-%d %H:%M:%S")
    return ds1

def bureau_data(request):
    """局数据"""
    #获取当前局点IP
    IP = extract_ip()
    #获取上次同步时间
    Last_Sync_Time = last_time()
    #合作伙伴信息
    PartnerInfo = "QQ音乐"
    #同步策略
    SyncPolicy = "局点信息同步数据到服务中台"

    return render(request, 'bureaudata.html',{"partner_info":PartnerInfo,"game_point_info":IP,"sync_policy":SyncPolicy,"last_sync_time":Last_Sync_Time})


def streamfree_recommended(request):
    is_login = request.session.get('is_login', '')
    username = request.session.get('name', '')

    #获取当前用户已经订购的产品
    if username:
        order_product = parse_user_OrderUnsubscribeInfo(username)
        #获取订购量Top3的产品
        queryset = OrderUnsubscribeInfo.objects.values('ProductId_x').annotate(c=Count('id')).order_by('-c')[:6]
        lis = []
        for item in queryset:
            ProductId = item.get('ProductId_x','')
            ProductName = ProductId_name.get(ProductId,'')
            lis.append(ProductName)
        productStr = ','.join(lis)
        return render(request, 'streamfree_recommended.html', {"is_login": is_login, "username": username, "orderProduct":order_product, "productStr":productStr})
    else:
        return render(request, 'streamfree_recommended.html')
    


def test(request):
    return render(request, 'test.html')


user_mobile = {
    "15638763580":"5B012E6D4CF86E78964C9350192E77E4",
    "17856923759":"57EE24FEC6B03FF998D1D8218B4CF8C7"
}

def get_username(username):
    return OrderUnsubscribeInfo.objects.filter(UserPseudoCode_x=username)

def parse_user_OrderUnsubscribeInfo(username_mobile):
    """
    从mysql数据库中获取数据并解析
    """

    #指定具体用户名并获取用户信息
    # username = '5B012E6D4CF86E78964C9350192E77E4'
    #手机号和用户伪码转换
    username = user_mobile.get(username_mobile,'')

    userinfo_queryset = get_username(username=username)
    serializer = OrderUnsubscribeInfoModelSerializer(userinfo_queryset, many=True)
    datas_old = json.dumps(serializer.data)
    datas = json.loads(datas_old)

    if datas:
        lis = []
        for data in datas:
            EffectiveRealTime  = data.get('EffectiveRealTime','')
            ProductId = data.get('ProductId_x','')
            lis.append(ProductId)
        pro_lis = []
        for i in list(set(lis)):
            pro_lis.append(ProductId_name.get(i,'移动新款铂金卡'))
        product_str = '+'.join(list(pro_lis))
        strs = f"互联网用户：{username_mobile}在{EffectiveRealTime },已经订购了{product_str} 移动定向流量产品"
        return strs

# def parse_user_OrderUnsubscribeInfo(username):
#     """
#     从mysql数据库中获取数据并解析
#     """

#     #指定具体用户名并获取用户信息
#     # username = '5B012E6D4CF86E78964C9350192E77E4'
#     userinfo_queryset = get_username(username=username)
#     serializer = OrderUnsubscribeInfoModelSerializer(userinfo_queryset, many=True)
#     datas_old = json.dumps(serializer.data)
#     datas = json.loads(datas_old)

#     if datas:
#         url_lis = []
#         lis = []
#         for data in datas:
#             username = data.get('UserPseudoCode_x','')
#             ActionTime = data.get('ActionTime','')
#             # ActionID = data.get('ActionID','')
#             # OrderType = data.get('OrderType','')  #0 测试 1 正式 
#             # hRet = data.get('hRet','')   #0表示成功；其他表示失败
#             url = data.get('url','')
#             if 'music.163' in url:
#                 url_lis.append('网易云音乐渠道')
#             elif 'kugou' in url:
#                 url_lis.append('酷狗音乐渠道')
#             elif 'kuwo' in url:
#                 url_lis.append('酷我音乐渠道')
#             elif 'qq' in url:
#                 url_lis.append('QQ音乐渠道')
#             elif 'taobao' in url:
#                 url_lis.append('淘宝商城渠道')
#             elif 'iqiyi' in url:
#                 url_lis.append('爱奇艺渠道')
#             elif 'vivo' in url:
#                 url_lis.append('VIVO渠道')
#             elif 'douyu' in url:
#                 url_lis.append('斗鱼渠道')
#             elif 'gitshow' in url:
#                 url_lis.append('快手渠道')
#             elif 'snssdk' in url:
#                 url_lis.append('今日头条渠道')
#             elif 'bilibili' in url:
#                 url_lis.append('哔哩哔哩渠道')
#             elif 'mgtv' in url:
#                 url_lis.append('芒果TV渠道')
#             elif 'ffapi' in url:
#                 url_lis.append('ffapi渠道')
#             elif 'bjk' in url:
#                 url_lis.append('网易白金星卡渠道')

#             ProductId = data.get('ProductId_x','')
#             lis.append(ProductId)
#         pro_lis = []
#         url_str = '+'.join(list(set(url_lis)))
#         for i in list(set(lis)):
#             pro_lis.append(ProductId_name.get(i,'移动新款铂金卡'))
#         product_str = '+'.join(list(pro_lis))
#         strs = f"时间：{ActionTime}, 用户：{username}，订购了{product_str}, 可以在{url_str}免流使用"
#         return strs

#网站首页
def web_index(request):
    is_login = request.session.get('is_login', '')
    username = request.session.get('name', '')

    #获取当前用户已经订购的产品
    if username:
        order_product = parse_user_OrderUnsubscribeInfo(username)
        #获取订购量Top3的产品
        queryset = OrderUnsubscribeInfo.objects.values('ProductId_x').annotate(c=Count('id')).order_by('-c')[:6]
        lis = []
        for item in queryset:
            ProductId = item.get('ProductId_x','')
            lis.append(ProductId)
        productStr = ','.join(lis)
        return render(request, 'index.html', {"is_login": is_login, "username": username, "orderProduct":order_product, "productStr":productStr})
    else:
        return render(request, 'index.html')

#实时推送, 
def realtimepush(request):
    # return HttpResponse("hello")
    return render(request, 'realtimepush.html')

#echarts可视化页面
def echartsindex(request):
    return render(request, 'echartsindex.html')

#echarts可视化页面
def echartsbarchartsindex(request):
    return render(request, 'echartsbarchartsindex.html')

def echartssalesbyproductchartsindex(request):
    return render(request, 'echartssalesbyproductchartsindex.html')

def echartsusersnumberchartsindex(request):
    return render(request, 'echartsusersnumberchartsindex.html')

def echartsflowsaleschartsindex(request):
    return render(request, 'echartsflowsaleschartsindex.html')

def echartscompetitivesalesbyproductchartsindex(request):
    return render(request, 'echartscompetitivesalesbyproductchartsindex.html')

def echartscompetitiveflowsaleschartsindex(request):
    return render(request, 'echartscompetitiveflowsaleschartsindex.html')

def echartcompetitivesusersnumberchartsindex(request):
    return render(request, 'echartcompetitivesusersnumberchartsindex.html')

class OrderUnsubscribeInfoList(GenericAPIView):
    # 2.指定查询集
    queryset = OrderUnsubscribeInfo.objects.all()
    # 3. 指定序列化器类
    serializer_class = OrderUnsubscribeInfoModelSerializer
    # 4. 指定过滤排序引擎
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # 5. 指定过滤字段
    filterset_fields = ['ActionTime', 'UserPseudoCode_x', 'url']
    # 6. 指定排序字段
    ordering_fields = ['ActionTime']

    def get(self, request):

        # 动态获取查询集
        qs = self.get_queryset()
        # 过滤查询集
        qs = self.filter_queryset(qs)
        # 序列化
        serializer = self.get_serializer(instance=qs, many=True)
        # 返回列表
        return Response(serializer.data, status=status.HTTP_200_OK)


class EchartsOrderUnsubscribe(GenericAPIView):
    """
        对应饼状图
    """
    def get(self,request):
        queryset= OrderUnsubscribeInfo.objects.all().values('ProductId_x').annotate(c=Count('id')).values_list('ProductId_x', 'c')
        dict_lis = []
        if queryset:
            for k,v in dict(queryset).items():
                dic = {"product":str(k),"count":v}
                dict_lis.append(dic)
        return JsonResponse({"datas":dict_lis}, safe=False)

def pro_dic(queryset):
    """
        累加个数
    """
    dict_lis = []
    count = 0
    if queryset:
        for k,v in dict(queryset).items():
            if v:
                count += int(v)
            else:
                count += 0
            dic = {"curtime":str(k),"count":count}
            dict_lis.append(dic)
    return dict_lis

class EchartsBarChartsOrderUnsubscribe(GenericAPIView):
    """
        对应条形图
    """
    
    def get(self,request):
        #按照时间段分组统计个数，以1小时为单位
        queryset= OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=['2022-07-01','2022-07-02']).annotate(hour=TruncHour('EffectiveRealTime')).values('hour').\
            annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        dict_lis = pro_dic(queryset)
        return JsonResponse({"datas":dict_lis}, safe=False)

def process_pandas(query_set):
    dic_query = {}
    c = 0
    for item in query_set:
        #时间
        c_time = str(item[0])
        #统计个数
        rawcount = item[1]
        #产品
        product_name = item[2]
        #放入字典
        dic_query.setdefault('c_time', []).append(c_time)
        dic_query.setdefault('rawcount', []).append(rawcount)
        dic_query.setdefault('product_name', []).append(product_name)
    df_datas = pd.DataFrame.from_dict(dic_query)
    df_datas['count'] = df_datas['rawcount'].cumsum()
    return df_datas

class EchartsSalesByProductOrderUnsubscribe(GenericAPIView):
    """
        运营分析：分产品销量走势(实时，无粒度)

        "500000050078":"移动花卡宝藏版29（月租型）",
        "500000050003":"移动花卡宝藏版2020-19元套卡",
        "100000001271":"随心看会员",
        "100000001125":"随心看会员-首月1元促销包",
        "100000001132":"动感地带5G通行证2020-30元",
        "100000091447":"随心听会员（15GB版）"
    """
    
    def get(self,request):
        cur_time = time.strftime('%X',time.localtime(time.time()))
        cur_time = datetime.time(*map(int, cur_time.split(':')))
        # queryset= OrderUnsubscribeInfo.objects.filter(ActionTime__lte=cur_time).values('ProductId_x').annotate(c=Count('id')).values_list('ProductId_x', 'c')
        queryset_baozangka = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-02','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=["500000050078","500000050003"]).annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        queryset_suixin = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-02','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=["100000000297","100000001125","100000091447"]).annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        queryset_donggan = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-02','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=["100000001132"]).annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
       
        dict_baozangka_lis = pro_dic(queryset_baozangka)
        dict_suixin_lis = pro_dic(queryset_suixin)
        dict_donggan_lis = pro_dic(queryset_donggan)

        return JsonResponse({"datas_baozangka":dict_baozangka_lis, "datas_suixin":dict_suixin_lis, "datas_donggan":dict_donggan_lis}, safe=False)

class EchartsUsersNumberOrderUnsubscribe(GenericAPIView):
    """
        运营分析：用户量(实时，无粒度)
    """
    
    def get(self,request):
        cur_time = time.strftime('%X',time.localtime(time.time()))
        cur_time = datetime.time(*map(int, cur_time.split(':')))
        #对用户去重
        queryset = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), \
            ActionTime__lte=cur_time).values('UserPseudoCode_x').distinct().annotate(hour=TruncHour('EffectiveRealTime')).\
                values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        query_dic = pro_dic(queryset)
        return JsonResponse({"datas":query_dic}, safe=False)

class EchartsFlowSalesOrderUnsubscribe(GenericAPIView):
    """
        运营分析：流量销量(实时，无粒度)
    """
    
    def get(self,request):
        cur_time = time.strftime('%X',time.localtime(time.time()))
        cur_time = datetime.time(*map(int, cur_time.split(':')))

        queryset = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time).\
            order_by('EffectiveRealTime').annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(S=Sum('unit_flow')).values_list('hour', 'S').order_by('EffectiveRealTime')

        query_dic = pro_dic(queryset)
        
        return JsonResponse({"datas":query_dic}, safe=False)

class EchartsCompetitiveSalesByProductOrderUnsubscribe(GenericAPIView):
    """
        竞品分析：产品销量(实时，无粒度)

        "500000050078":"移动花卡宝藏版29（月租型）",
        "500000050003":"移动花卡宝藏版2020-19元套卡",
        "100000001271":"随心看会员",
        "100000001125":"随心看会员-首月1元促销包",
        "100000001132":"动感地带5G通行证2020-30元",
        "100000091447":"随心听会员（15GB版）"
    """
    
    def get(self,request):
        cur_time = time.strftime('%X',time.localtime(time.time()))
        cur_time = datetime.time(*map(int, cur_time.split(':')))
        #模拟爱奇艺产品
        queryset_aqiyi = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=['500000050078','100000001132','500000050051','500000050003','100000091447','100000000297','100000001271','100000090135','100000090076']).\
            order_by('EffectiveRealTime').annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        #模拟优酷产品
        queryset_youku = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=['500000050003','100000091447','100000000297','100000001271','100000090135','100000090076']).\
            order_by('EffectiveRealTime').annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        #模拟腾讯产品
        queryset_tengxun = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=['100000001271','100000090135','100000090076']).\
            order_by('EffectiveRealTime').annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        
        
        query_aqiyi_dic = pro_dic(queryset_aqiyi)
        query_youku_dic = pro_dic(queryset_youku)
        query_tengxun_dic = pro_dic(queryset_tengxun)
        
        return JsonResponse({"datas1":query_aqiyi_dic, "datas2":query_youku_dic, "datas3":query_tengxun_dic}, safe=False)

class EchartsCompetitiveFlowSalesOrderUnsubscribe(GenericAPIView):
    """
        竞品分析：流量销量(实时，无粒度)
    """
    
    def get(self,request):
        cur_time = time.strftime('%X',time.localtime(time.time()))
        cur_time = datetime.time(*map(int, cur_time.split(':')))
        #爱奇艺
        queryset_aiqiyi = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=[500000050078,100000001132,500000050051,500000050003,100000091447,100000000297]).\
            order_by('EffectiveRealTime').annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(S=Sum('unit_flow')).values_list('hour', 'S').order_by('EffectiveRealTime')
        #优酷
        queryset_youku = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=[500000050003,100000091447,100000000297]).\
            order_by('EffectiveRealTime').annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(S=Sum('unit_flow')).values_list('hour', 'S').order_by('EffectiveRealTime')
        #腾讯
        queryset_tengxun = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=[100000001271,100000090135,100000090076]).\
            order_by('EffectiveRealTime').annotate(hour=TruncHour('EffectiveRealTime')).values('hour').annotate(S=Sum('unit_flow')).values_list('hour', 'S').order_by('EffectiveRealTime')

        query_aqiyi_dic = pro_dic(queryset_aiqiyi)
        query_youku_dic = pro_dic(queryset_youku)
        query_tengxun_dic = pro_dic(queryset_tengxun)
        
        return JsonResponse({"datas1":query_aqiyi_dic, "datas2":query_youku_dic, "datas3":query_tengxun_dic}, safe=False)

class EchartsCompetitiveUsersNumberOrderUnsubscribe(GenericAPIView):
    """
        竞品分析：用户量(实时，无粒度)
    """
    
    def get(self,request):
        cur_time = time.strftime('%X',time.localtime(time.time()))
        cur_time = datetime.time(*map(int, cur_time.split(':')))
        #对用户去重
        #爱奇艺用户
        queryset_aqiyi = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=[500000050078,100000001132,500000050051,500000050003,100000091447,100000000297]).values('UserPseudoCode_x').distinct().annotate(hour=TruncHour('EffectiveRealTime')).\
                values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        #优酷用户
        queryset_youku = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=[500000050003,100000091447,100000000297]).values('UserPseudoCode_x').distinct().annotate(hour=TruncHour('EffectiveRealTime')).\
                values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        #腾讯用户
        queryset_tengxun = OrderUnsubscribeInfo.objects.filter(EffectiveRealTime__range=('2022-07-01','2022-07-03'), ActionTime__lte=cur_time, ProductId_x__in=[100000001271,100000090135,100000090076]).values('UserPseudoCode_x').distinct().annotate(hour=TruncHour('EffectiveRealTime')).\
                values('hour').annotate(c=Count('id')).values_list('hour', 'c').order_by('EffectiveRealTime')
        query_aqiyi_dic = pro_dic(queryset_aqiyi)
        query_youku_dic = pro_dic(queryset_youku)
        query_tengxun_dic = pro_dic(queryset_tengxun)
        
        return JsonResponse({"datas1":query_aqiyi_dic, "datas2":query_youku_dic, "datas3":query_tengxun_dic}, safe=False)
