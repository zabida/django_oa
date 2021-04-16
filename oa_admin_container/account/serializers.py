from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_encode_handler

from oa_admin.customer import errors


class LoginSerializer(serializers.Serializer):
    """登录序列化，获取jwt—token"""
    login_type = serializers.IntegerField(required=False, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def save(self, **kwargs):
        username, password = self.validated_data.get('username'), self.validated_data.get('password')
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise errors.raise_validation_error('用户不存在')

        if not user.check_password(password):
            raise errors.raise_validation_error('密码不正确')

        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
        }
        data = {
            'token': jwt_encode_handler(payload)
        }
        return data


class RegisterSerializer(serializers.Serializer):

    type = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)

    def save(self, **kwargs):
        user_data = self.validated_data
        type_ = user_data.get('type')
        if type_ == '1':
            pass
        username = user_data.get('username')
        if User.objects.filter(username=username).first():
            raise errors.raise_validation_error('用户名已存在')
        else:
            User.objects.create_superuser(**user_data)
        return {'msg': '创建成功'}
