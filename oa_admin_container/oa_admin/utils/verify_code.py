from django.core.cache import cache

from oa_admin.customer import errors


def code_check(code_url, code):
    if code != cache.get(code_url):
        raise errors.raise_validation_error('验证码错误！')
    else:
        return True
