import hashlib

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils.encoding import force_bytes


class User(AbstractBaseUser):
    TYPE_USER = '0'
    TYPE_ENTER = '1'
    TYPE_ADMIN = '2'
    TYPE_NOTENTER = '3'

    TYPE_CHOICES = (
        (TYPE_USER, '个人用户'),
        (TYPE_ENTER, '企业用户-法人'),
        (TYPE_ADMIN, '管理员'),
        (TYPE_NOTENTER, '企业用户-非法人'),
    )

    STATUS_LOW = '0'
    STATUS_MEDI = '1'
    STATUS_HIGH = '2'
    STATUS_IN_AUTH = '3'
    STATUS_AUTH_FAILURE = '4'

    STATUS_CHOICES = (
        (STATUS_LOW, '未认证'),
        (STATUS_MEDI, '已认证[中]'),
        (STATUS_HIGH, '已认证[高]'),
        (STATUS_IN_AUTH, '认证中'),
        (STATUS_AUTH_FAILURE, '认证失败'),
    )

    AUTHENTIC_FACE = '0'
    AUTHENTIC_UNIONPAY = '1'
    AUTHENTIC_ENTERPRISE = '2'
    AUTHENTIC_ALIPAY = '3'
    AUTHENTIC_WECHAT = '4'
    AUTHENTIC_UNVERIFIED = '5'
    AUTHENTIC_ALIPAY_OATH = '33'  # 个人中心首次绑定支付宝

    AUTHENTIC_CHOICES = (
        (AUTHENTIC_FACE, 'CA个人扫脸认证'),
        (AUTHENTIC_UNIONPAY, 'CA银联卡认证'),
        (AUTHENTIC_ENTERPRISE, 'CA企业认证'),
        (AUTHENTIC_ALIPAY, '支付宝认证'),
        (AUTHENTIC_WECHAT, '管理员验证'),
        (AUTHENTIC_UNVERIFIED, '未认证'),
        (AUTHENTIC_ALIPAY_OATH, '绑定支付宝'),
    )

    # 用户id主键
    id = models.AutoField(primary_key=True)
    # 用户uuid
    user_uuid = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text='用户uuid')
    # 用户code
    user_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    # 用户名
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    # 手机号
    cellphone = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    # 电子邮箱
    email = models.CharField(max_length=200, null=True, blank=True)
    # 真实姓名
    real_name = models.CharField(max_length=20, null=True, blank=True)
    # 身份证号
    id_card = models.CharField(max_length=50, null=True, blank=True)
    # 微信uuid
    wechat_uuid = models.CharField(max_length=100, null=True, blank=True)
    # 微信昵称
    wechat_name = models.CharField(max_length=100, null=True, blank=True)
    # 支付宝uuid
    alipay_uuid = models.CharField(max_length=100, null=True, blank=True)
    # 支付宝昵称
    alipay_name = models.CharField(max_length=100, null=True, blank=True)

    # 认证方式 '0': CA个人扫脸认证; '1': CA银联卡实名认证; '2': CA企业认证; '3': 支付宝认证; '4': 管理员审核认证; '5': '未认证'
    authentic = models.CharField(max_length=10, choices=AUTHENTIC_CHOICES, default=AUTHENTIC_UNVERIFIED)
    # 认证时间
    authentic_time = models.DateTimeField(null=True, blank=True)
    # 用户类型 '0': 个人用户; '1': 企业用户; '2': 管理员用户
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_USER)
    # 用户状态 '0': 未认证, 低; '1': 已认证, 中; '2': 高
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_LOW)
    # 版本号用于退出
    version_number = models.IntegerField(default=0)
    # 是否已经冻结
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'id'
    objects = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ('-created_at',)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def check_password(self, password):
        raw_password = hashlib.md5(force_bytes(password)).hexdigest().upper()

        return raw_password == self.password.upper()
