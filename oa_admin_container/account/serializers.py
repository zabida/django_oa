from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_encode_handler


class LoginSerializer(serializers.Serializer):
    """登录序列化，获取jwt—token"""
    login_type = serializers.IntegerField(required=False, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def save(self, **kwargs):
        username, password = self.validated_data.get('username'), self.validated_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception('不存在')

        if not user.check_password(password):
            raise Exception('密码不正确')

        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
        }
        data = {
            'token': jwt_encode_handler(payload)
        }
        return data

