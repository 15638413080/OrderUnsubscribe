from django.contrib.auth.models import User, Group
from queue import PriorityQueue
from rest_framework import viewsets
from users.serializers import UserModelSerializer

from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from .serializers import UserModelSerializer, OrderUnsubscribeInfoModelSerializer
from .models import User, OrderUnsubscribeInfo
from django.contrib.auth.hashers import check_password

from django.contrib.auth import logout
from django.shortcuts import redirect, render
from .form import UserLoginForm, UserRegisterForm
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from  .serializers import  UserSerializer, GroupSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from users.utils.jwt_create_token import create_token
from users.extensions.jwt_authenticate import JWTQueryParamsAuthentication
import datetime


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def registerdata(request):
    if request.method == "GET":
        return JsonResponse({'msg': '请使用post方式提交表单数据', 'code': 400}, json_dumps_params={"ensure_ascii":False})
    else:
        userregisterForm = UserRegisterForm(request.POST)

        if request.POST["username"] and request.POST["password"]:  # 进行数据校验
            username = request.POST["username"]
            password = request.POST["password"]
            nickname = request.POST["nickname"]
            if User.objects.filter(username=username):
                # return JsonResponse({'msg': '该用户已注册！', 'code': 400}, json_dumps_params={"ensure_ascii":False})
                return redirect('/api/loginforms/')
            else:
                user_data = {'username': username, 'password': make_password(password), 'nickname': nickname}
                user_serializer = UserModelSerializer(data=user_data)
                print(user_serializer)
                if user_serializer.is_valid():
                    user_serializer.save()
                    # return JsonResponse({'msg': '注册成功！', 'code': 200}, json_dumps_params={"ensure_ascii":False})
                    return redirect('/api/loginforms/')
                else:
                    return JsonResponse({'msg': user_serializer.errors, 'code': 400}, json_dumps_params={"ensure_ascii":False})
        else:
            print(userregisterForm.errors)    # 打印错误信息
            clean_errors = userregisterForm.errors
            return JsonResponse({"userregisterForm": userregisterForm, "clean_errors": clean_errors}, json_dumps_params={"ensure_ascii":False})


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        nickname = request.data.get('nickname')
        if User.objects.filter(username=username):
            return Response({'msg': '该用户已注册！', 'code': 400})
        else:
            if password1 == password2:
                user_data = {'username': username, 'password': make_password(password1), 'nickname': nickname}
                user_serializer = UserModelSerializer(data=user_data)
                if user_serializer.is_valid():
                    user_serializer.save()
                    # return Response({'msg': '注册成功！', 'code': 200})
                    return redirect('/api/loginforms/')
                else:
                    return Response({'msg': user_serializer.errors, 'code': 400})
            else:
                return Response({'msg': '两次密码不一致！', 'code': 400})

user_mobile = {
    "15638763580":"5B012E6D4CF86E78964C9350192E77E4",
    "17856923759":"57EE24FEC6B03FF998D1D8218B4CF8C7"
}

def submitdata(request):

    if request.method == "GET":
        return JsonResponse({'msg': '请使用post方式提交表单数据', 'code': 400}, json_dumps_params={"ensure_ascii":False})
    else:
        userloginForm = UserLoginForm(request.POST)

        if request.POST["username"] and request.POST["password"]:  # 进行数据校验
            username = request.POST["username"]
            password = request.POST["password"]
            #手机号和用户伪码转换
            user_pseudo_code = user_mobile.get(username,'')
            user = User.objects.filter(username=user_pseudo_code).first()
            if user and check_password(password, user.password):
                # return Response({'msg': '登录成功', 'code': 200, 'user_id': user.id})
                #设置session
                request.session['is_login'] = True
                request.session['name'] = username
                # return redirect('/api/streamfree_recommended')
                return redirect('/index')
            else:
                # return JsonResponse({'msg': '登录失败', 'code': 400}, json_dumps_params={"ensure_ascii":False})
                return redirect('/api/loginforms')
            
        else:
            print(userloginForm.errors)    # 打印错误信息
            clean_errors = userloginForm.errors
            return JsonResponse({"userloginForm": userloginForm, "clean_errors": clean_errors}, json_dumps_params={"ensure_ascii":False})
        

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            return Response({'msg': '登录成功', 'code': 200, 'user_id': user.id})
        else:
            return Response({'msg': '登录失败', 'code': 400})

    # 生成记录登录状态的token

# 视图名不能起成logout
def logoutView(request):
    logout(request) # 调用django自带退出功能，会帮助我们删除相关session
    return redirect(request.META["HTTP_REFERER"])

def loginForms(request):
    userLoginForm = UserLoginForm()
    return render(request, 'loginforms.html', {"userLoginForm":userLoginForm})

def registerForms(request):
    userRegisterForm = UserRegisterForm()
    return render(request, 'registerforms.html', {"userRegisterForm":userRegisterForm})

class OrderUnsubscribeInfoView(GenericAPIView, ListModelMixin):
    """
    Concrete view for listing a queryset.
    """
    queryset = OrderUnsubscribeInfo.objects.all()
    serializer_class = OrderUnsubscribeInfoModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenViewBase):
    """
    自定义刷新token refresh: 刷新token的元素
    """
    serializer_class = MyTokenRefreshSerializer

class ProLoginView(APIView):
    """用户登录"""
    # authentication_classes = [] # 取消全局认证
    permission_classes = []
    authentication_classes = [JWTQueryParamsAuthentication,]
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj and check_password(password, user_obj.password):
            payload = {
                'user_id':user_obj.id,#自定义用户ID
                'username':user_obj.username,#自定义用户名
                'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=10),# 设置超时时间，1min
            }
            jwt_token = create_token(payload=payload)
            return Response({'code':200,'token':jwt_token})
        else:
            return Response({'code':401,'error':'用户名或密码错误'})

class ProRegisterView(APIView):
    authentication_classes = [] # 取消全局认证
    permission_classes = []
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj and check_password(password, user_obj.password):

            payload = {
                'user_id':user_obj.pk,#自定义用户ID
                'username':user_obj.username,#自定义用户名
                'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=1),# 设置超时时间，1min
            }
            jwt_token = create_token(payload=payload)
            return Response({'code':200,'token':jwt_token})

        else:
            return Response({'code':401,'error':'用户名或密码错误'})

class ProIndexView(APIView):
	# 局部认证
    authentication_classes = [JWTQueryParamsAuthentication,]
    def get(self,request,*args,**kwargs):
        return Response("可以了")
