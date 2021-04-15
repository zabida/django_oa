from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from account.serializers import LoginSerializer, RegisterSerializer
from oa_admin.utils.verify_code import code_check


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
    http_method_names = ['post', 'put']

    def create(self, request, *args, **kwargs):
        pass