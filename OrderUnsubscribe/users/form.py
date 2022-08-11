from django.forms import Form, ModelForm
from django.forms import fields
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import get_user_model


# class RegisterForm(Form):
#     username = fields.CharField(
#         required=True,
#         min_length=3,
#         max_length=18,
#         error_messages={
#             "required":"用户名不可以为空！",
#             "min_length":"用户名不能低于3位！",
#             "max_length":"用户名不能超过18位！"
#         }
#     )
#     password1 = fields.CharField(
#         required=True,
#         min_length=3,
#         max_length=128,
#         error_messages={
#             "required":"密码不可以空",
#             "min_length": "密码不能低于3位！",
#             "max_length": "密码不能超过18位！"
#         }
#     )
#     password2 = fields.CharField(required=False)

#     def clean_password2(self):
#         if not self.errors.get("password1"):
#             if self.cleaned_data["password2"] != self.cleaned_data["password1"]:
#                 raise ValidationError("您输入的密码不一致，请重新输入！")
#             return self.cleaned_data

class UserLoginForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class UserRegisterForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password','nickname']

# class LoginForm(Form):
#     username = fields.CharField(
#         required=True,
#         min_length=3,
#         max_length=18,
#         error_messages={
#             "required":"用户名不可以为空！",
#             "min_length":"用户名不能低于3位！",
#             "max_length":"用户名不能超过18位！"
#         }
#     )
#     password = fields.CharField(
#         required=True,
#         error_messages={
#             "required":"密码不可以空",
#         }
#     )
