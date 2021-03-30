from django.db import models


class Permission(models.Model):

    name = models.CharField(help_text='权限名字', blank=False, null=False, unique=True)
    code = models.CharField(help_text="权限code", blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'permission'


class Role(models.Model):
    role_name = models.CharField(help_text='角色名称', blank=False, null=False, unique=True)
    permission = models.CharField(help_text='权限', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

