import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'tutorial.settings')

import django

django.setup()

from account import models as acc_mod
from snippets import models as sni_mod

objs = acc_mod.User.objects.filter()
objs.filter(password=12345).update(password=1)   # 返回更新个数
print(objs)
for i in objs.all():
    print(i.__dict__)