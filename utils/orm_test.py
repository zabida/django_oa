import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'tutorial.settings')

import django

django.setup()

from account import models as acc_mod
from snippets import models as sni_mod


user = acc_mod.User.objects.get(pk=1)
print(user)

sni = sni_mod.Snippet.objects.get(pk=1)
print(sni.owner)
print(sni.owner_id)


# 反向查询
user: sni_mod.Snippet = acc_mod.User.objects.get(pk=1)
# print(user.snippet_set.all())
print(user.owner_snippets.all())