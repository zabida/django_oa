import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication, get_authorization_header
from rest_framework.settings import api_settings

from oa_admin.customer.errors import raise_authentication_error

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class MyAuthentication(BasicAuthentication):
    """
    header中添加x-username参数校验
    """
    # def authenticate(self, request):
    #     username = request.META.get('HTTP_X_USERNAME')
    #     if not username:
    #         return None
    #
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         raise exceptions.AuthenticationFailed('No such user')
    #
    #     return user, None
    @ staticmethod
    def get_jwt_value(request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = 'Invalid Authorization header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        jwt_value =MyAuthentication.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('过期')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('error decode')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('invalid token')

        user = self.my_authenticate_credentials(payload)
        return user, jwt_value

    @staticmethod
    def my_authenticate_credentials(payload):
        User = get_user_model()
        user_id = payload.get('user_id', '')
        version_number = payload.get('version_number', '')

        if not user_id:
            raise raise_authentication_error(msg='非法操作!')

        try:
            user = User.objects.get(id=user_id)
            if user.version_number != version_number:
                raise raise_authentication_error(msg='token已过期')
            if user.is_active:
                raise raise_authentication_error(msg='您的账户已经冻结，若有任何疑问可联系平台客服sjkf@shanghai.gov.cn')
        except User.DoesNotExist:
            raise raise_authentication_error(msg='非法操作!')
        return user
