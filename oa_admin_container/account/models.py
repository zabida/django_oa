from django.db import models


class Permission(models.Model):

    name = models.CharField(help_text='权限名字', blank=False, null=False, unique=True)
    code = models.CharField(help_text="权限code", blank=False, null=False, unique=True)
    parent_id = models.IntegerField()
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'permission'


class Role(models.Model):
    role_name = models.CharField(help_text='角色名称', blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role'


class RolePermission(models.Model):
    role_id = models.IntegerField()
    permission_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role_permission'


class UserRole(models.Model):
    user_id = models.IntegerField()
    role_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_role'


class Group(models.Model):
    group_name = models.CharField(help_text='组名', blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group'


class GroupRole(models.Model):
    group_id = models.IntegerField()
    role_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group_role'


class GroupUser(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'group_user'
