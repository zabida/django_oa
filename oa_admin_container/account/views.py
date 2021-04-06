from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from account.serializers import LoginSerializer, RegisterSerializer


class Authentication(generics.ListCreateAPIView):
    http_method_names = ['post', 'put']

    def create(self, request, *args, **kwargs):
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
