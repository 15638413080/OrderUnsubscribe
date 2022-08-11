from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import User, OrderUnsubscribeInfo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name')

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OrderUnsubscribeInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderUnsubscribeInfo
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token

    def validate(self, attrs):
        """
        登录返回token和refresh
        :param attrs:
        :return:
        """
        data = super().validate(attrs)
        data['token'] = str(data["access"])
        return data

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    serializer_class = MyTokenObtainPairSerializer