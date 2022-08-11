from dataclasses import fields
from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField

class UserManager(BaseUserManager):
    def _create_user(self,username,password,**kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")

        user = self.model(username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,username,password,email,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username,password,email,**kwargs)

    def create_superuser(self,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username,password,**kwargs)

class User(AbstractBaseUser,PermissionsMixin): # 继承AbstractBaseUser，PermissionsMixin

    id = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=32,verbose_name="用户名",unique=True)
    password = models.CharField(max_length=128, verbose_name="用户密码")
    nickname = models.CharField(max_length=13,verbose_name="昵称",null=True,blank=True)

    is_active = models.BooleanField(default=True,verbose_name="激活状态")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True,verbose_name="是否是员工")
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class OrderUnsubscribeInfo(models.Model):

    id = models.AutoField(primary_key=True)
    TraceId = models.CharField(max_length=32, default='')
    ActionTime = models.TimeField(auto_now_add = False, auto_now = False)
    MsgType_x = models.CharField(max_length=32, default='')
    MsgType_y = models.CharField(max_length=32, default='')
    Version_x = models.CharField(max_length=32, default='')
    Version_y = models.CharField(max_length=32, default='')
    OrderID = models.CharField(max_length=32, default='')
    UserPseudoCode_x = models.CharField(max_length=32, default='')
    UserPseudoCode_y = models.CharField(max_length=32, default='')
    ActionID = models.CharField(max_length=32, default='')
    EffectiveRealTime = models.DateTimeField(auto_now_add=False, auto_now = False)
    ExpireRealTime = models.CharField(max_length=64, default='')
    ChannelId = models.CharField(max_length=32, default='')
    ProductId_x = models.CharField(max_length=32, default='')
    ProductId_y = models.CharField(max_length=32, default='')
    OrderType = models.CharField(max_length=32, default='')
    sign = models.CharField(max_length=64, default='')
    ProvCode = models.CharField(max_length=32, default='')
    hRet = models.CharField(max_length=32, default='')
    desc = models.CharField(max_length=32, default='')
    url = models.CharField(max_length=128, default='')
    unit_flow = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # def __str__(self):
    #     return str(self.ActionTime)

    class Meta:
        db_table = 'if2_message'
