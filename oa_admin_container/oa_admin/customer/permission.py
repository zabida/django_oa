from django.contrib.auth.models import User
from rest_framework import permissions


class BlacklistPermission(permissions.BasePermission):

    message = 'blacklist user not allowed'

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blocked = User.objects.filter().exists()
        return blocked
