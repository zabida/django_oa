import logging

from django.http import Http404
from django.utils.encoding import force_text
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework.response import Response
from rest_framework import exceptions, status

logger = logging.getLogger('django')


class _ServerError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, error_code=None, detail=None):
        if not error_code:
            self.error_code = self.status_code
        else:
            self.error_code = error_code
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)


def exception_handler(exc, context):
    if isinstance(exc, exceptions.AuthenticationFailed) or isinstance(exc, exceptions.NotAuthenticated):
        data = {'msg': 'Authenticate failed'}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, Http404):
        data = {'detail': '未找到'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'msg': exc.detail}
        if isinstance(exc, _ServerError):
            return Response(data, status=exc.status_code, headers=headers)
        else:
            return Response(data, status=exc.status_code, headers=headers)
    elif isinstance(exc, PermissionDenied):
        data = {'msg': 'Permission denied.'}
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    else:
        logger.error(exc)
        return Response({'msg': '内部错误'}, status=status.HTTP_501_NOT_IMPLEMENTED)