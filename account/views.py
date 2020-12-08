from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny

from tutorial import errors
from tutorial.response import JSONResponse
from .serializers import User, AccountPersonalSerializer
from utils.remove_sc import special_characters


class AccountViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = AccountPersonalSerializer
    permission_classes = (AllowAny, )
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        special_characters(request)
        serializer = AccountPersonalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JSONResponse({'msg': 'success'}, status=status.HTTP_200_OK)


class AlipayViewSet(viewsets.ModelViewSet):
    pass
