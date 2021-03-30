from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from account.serializers import LoginSerializer


class Authentication(generics.ListCreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data=data)
