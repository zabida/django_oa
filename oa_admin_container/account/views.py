import base64
import threading
import uuid
from django.core.cache import cache
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response

from account.serializers import LoginSerializer, RegisterSerializer
from oa_admin.utils.verify_code import code_check
from oa_admin.utils.verify_img import CodeImg


class Authentication(generics.ListCreateAPIView):
    http_method_names = ['post', 'put']

    def create(self, request, *args, **kwargs):
        code_url = request.data.get('code_url')
        code = request.data.get('code')
        code_check(code_url=code_url, code=code)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data=data)


class Register(generics.ListCreateAPIView):
    http_method_names = ['post', 'put']

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data=data)


class Code(generics.ListCreateAPIView):
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        img_id = uuid.uuid4()
        code_img = CodeImg()
        img, code = code_img.get_valid_code_img()
        cache.set(img_id, code, timeout=settings.CODE_TIMEOUT)
        _ret = {
            'img': base64.b64encode(img),
            'img_uuid': img_id
        }
        threading.Thread()
        return Response(data=_ret)
