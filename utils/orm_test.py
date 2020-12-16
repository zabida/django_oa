import os

from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'tutorial.settings')

import django

django.setup()

from account import models as acc_mod
from snippets import models as sni_mod

# objs = acc_mod.User.objects.filter()
# objs.filter(password=12345).update(password=1)   # 返回更新个数
# print(objs)
# for i in objs.all():
#     print(i.__dict__)

objs = acc_mod.User.objects.filter()

pp = ['1', '1234']
q = Q()
for p in pp:
    q |= Q(password=p)

# objs = objs.filter(q)
# for i in objs:
#     print(i)

a = objs.values_list('password', flat=True).order_by('password').distinct()
print(a)
