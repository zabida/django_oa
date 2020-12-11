import os
import django
from account import models as acc_mod
from snippets import models as sni_mod

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'tutorial.settings')
django.setup()

user = acc_mod.User.objects.get(pk=1)
print(user)

sni = sni_mod.Snippet.objects.get(pk=1)
print(sni.owner)
print(sni.owner_id)


# 反向查询
user: sni_mod.Snippet = acc_mod.User.objects.get(pk=1)
# print(user.snippet_set.all())  默认是小写的类名_set
print(user.owner_snippets.all())   # 定义模型时Snippet里定义了owner_snippets关系名

a = sni_mod.Snippet.objects.filter(title='haha').values('id', 'code', 'created')
# a = [{'id': '', 'code': '', 'created': ''}, {}, {}]
b = sni_mod.Snippet.objects.filter(title='haha').values_list('id', 'code', 'created')
# b = [('id', 'code', 'created'), (), ()...]
c = sni_mod.Snippet.objects.filter(title='haha').values_list('code', flat=True)
# c = ['code', ...]
