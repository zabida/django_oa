from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication


class MyAuthentication(BasicAuthentication):
    """
    header中添加x-username参数校验
    """
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
