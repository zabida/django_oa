from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    objects = models.Manager()

    class Meta:
        ordering = ['created']


class UserToken(models.Model):
    """
    用户的token信息,用于调用api接口
    """
    STATUS_AVA = '1'
    STATUS_UNAVA = '0'

    STATUS_CHOICE = (
        (STATUS_AVA, '可用'),
        (STATUS_UNAVA, '不可用'),
    )
    # 主键
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_token', null=True, blank=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, null=True, blank=True)
    effective_date = models.DateField(verbose_name='token生效日期', default=timezone.now)
    expire_date = models.DateField(verbose_name='token过期日期', default=timezone.now)
    status = models.CharField(max_length=2, verbose_name='可用状态', choices=STATUS_CHOICE, default=STATUS_AVA)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_time = models.DateTimeField(verbose_name='上次短信通知时间', blank=True, null=True)

    class Meta:
        db_table = 'user_token'
        # ordering = ('-created_at',)
