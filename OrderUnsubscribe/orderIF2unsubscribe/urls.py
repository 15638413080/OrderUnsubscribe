"""orderIF2unsubscribe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users import views as usersviews
from users import form as usersforms
from websocketUnsubscribe import views as websocketviews

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from  rest_framework.routers import DefaultRouter

group_router = DefaultRouter()
group_router.register('GroupsInfo',usersviews.GroupViewSet,basename='GroupsInfo')

urlpatterns = [
    path('admin/', admin.site.urls),
    #网站首页
    path('index/',websocketviews.web_index , name='index'),
    # 用户登录页面
    path('api-auth/', include('rest_framework.urls')),
    #使用pyjwt实现
    path('api/proorder/',usersviews.ProIndexView.as_view() , name='proorder'),
    path('api/prologin/',usersviews.ProLoginView.as_view() , name='prologin'),
    #user JWT验证
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/', usersviews.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    #users应用配置
    path('api/register/',usersviews.RegisterView.as_view() , name='register'),
    path('api/login/',usersviews.LoginView.as_view() , name='login'),
    path('api/loginforms/',usersviews.loginForms , name='loginforms'),  #动态生成登录表单
    path('api/registerforms/',usersviews.registerForms , name='registerforms'),  #动态生成注册表单
    # path('api/registerforms/',usersviews.ProRegisterView.as_view(), name='registerforms'),  #动态生成登录表单
    path('api/loginforms/submitdata/',usersviews.submitdata , name='loginsubmit'), #登录提交数据
    # path('api/loginforms/submitdata/',usersviews.ProLoginView.as_view() , name='loginsubmit'), #登录提交数据
    path('api/registerforms/registerdata/',usersviews.registerdata , name='registersubmit'), #注册提交数据
    #退出登录
    path('api/logout/',usersviews.logoutView , name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/orderUnsubscribeInfo/',usersviews.OrderUnsubscribeInfoView.as_view() , name='orderUnsubscribeInfo'),
    #channels应用配置
    path('api/websocket/',websocketviews.OrderUnsubscribeInfoList.as_view() , name='websocket'),
    #realtimepush页面
    path('api/websocket/realtimepush/', websocketviews.realtimepush, name="realtimepush"),
    #echarts图表页面获取json数据
    path('api/echarts/',websocketviews.EchartsOrderUnsubscribe.as_view() , name='echarts'), 
    #路由到echartsindex.html页面，动态加载echarts后台Json数据
    path('api/echartsindex/',websocketviews.echartsindex , name='echartsindex'),
    #以hour分组统计个数条形图
    path('api/echartsbarcharts/',websocketviews.EchartsBarChartsOrderUnsubscribe.as_view() , name='echartsbar'),
    #路由到echartsbarcharts.html页面，动态加载数据
    path('api/echartsbarchartsindex/',websocketviews.echartsbarchartsindex , name='echartsbarindex'),
    #分产品销量实时走势图
    path('api/echartssalesbyproductcharts/',websocketviews.EchartsSalesByProductOrderUnsubscribe.as_view() , name='echartssalesbyproductcharts'),
    #路由到echartssalesbyproductchartsindex.html页面，动态加载数据
    path('api/echartssalesbyproductchartsindex/',websocketviews.echartssalesbyproductchartsindex , name='echartssalesbyproductchartsindex'),
    #用户量实时走势图
    path('api/echartsusersnumbercharts/',websocketviews.EchartsUsersNumberOrderUnsubscribe.as_view() , name='echartsusersnumbercharts'),
    #路由到echartsusersnumberchartsindex.html页面，动态加载数据
    path('api/echartsusersnumberchartsindex/',websocketviews.echartsusersnumberchartsindex , name='echartsusersnumberchartsindex'),
    #流量实时走势图
    path('api/echartsflowsalescharts/',websocketviews.EchartsFlowSalesOrderUnsubscribe.as_view() , name='echartsflowsalescharts'),
    #路由到echartsflowsaleschartsindex.html页面，动态加载数据
    path('api/echartsflowsaleschartsindex/',websocketviews.echartsflowsaleschartsindex , name='echartsflowsaleschartsindex'),
    #竞品分析，产品销量实时走势图
    path('api/echartscompetitivesalesbyproductcharts/',websocketviews.EchartsCompetitiveSalesByProductOrderUnsubscribe.as_view() , name='echartscompetitivesalesbyproductcharts'),
    #echartscompetitivesalesbyproductchartsindex.html页面，动态加载数据
    path('api/echartscompetitivesalesbyproductchartsindex/',websocketviews.echartscompetitivesalesbyproductchartsindex , name='echartscompetitivesalesbyproductchartsindex'),
    #竞品分析：流量实时走势图
    path('api/echartscompetitiveflowsalescharts/',websocketviews.EchartsCompetitiveFlowSalesOrderUnsubscribe.as_view() , name='echartscompetitiveflowsalescharts'),
    #路由到echartscompetitiveusersnumberchartsindex.html页面，动态加载数据
    path('api/echartscompetitiveflowsaleschartsindex/',websocketviews.echartscompetitiveflowsaleschartsindex , name='echartscompetitiveflowsaleschartsindex'),
    #竞品分析：用户量实时走势图
    path('api/echartscompetitiveusersnumbercharts/',websocketviews.EchartsCompetitiveUsersNumberOrderUnsubscribe.as_view() , name='echartscompetitiveusersnumbercharts'),
    #路由到echartcompetitivesusersnumberchartsindex.html页面，动态加载数据
    path('api/echartscompetitiveusersnumberchartsindex/',websocketviews.echartcompetitivesusersnumberchartsindex , name='echartscompetitiveusersnumberchartsindex'),

    path('api/test/',websocketviews.test , name='test'),
    #免流/推荐展示页面
    path('api/streamfree_recommended/',websocketviews.streamfree_recommended , name='streamfree_recommended'),
    #局数据同步页面展示
    path('api/bureau_data/',websocketviews.bureau_data , name='bureau_data'),
    
]
