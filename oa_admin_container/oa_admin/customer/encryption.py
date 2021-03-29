#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@time : 2020/5/4 13:32
@file : encryption.py

实现参考:
    1. https://docs.djangoproject.com/en/3.0/howto/custom-model-fields/
    2. django-cryptography包中利用装饰器完成加密思路
"""

import typing

from django.core import checks
from django.db import models
from django.utils.translation import ugettext_lazy as _

FIELD_CACHE = {}


class EncryptedMixin(object):
    """
    A field mixin storing encrypted data

    :param bytes key: This is an optional argument.

        Allows for specifying an instance specific encryption key.
    :param int ttl: This is an optional argument.

        The amount of time in seconds that a value can be stored for. If the
        time to live of the data has passed, it will become unreadable.
        The expired value will return an :class:`Expired` object.
    """

    def __init__(self, *args, **kwargs):
        self.encrypt = EncryptTool()
        super().__init__(*args, **kwargs)

    @property
    def description(self):
        return _('Encrypted %s') % super().description

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if getattr(self, 'remote_field', None):
            errors.append(
                checks.Error(
                    'Base field for encrypted cannot be a related field.',
                    hint=None,
                    obj=self,
                    id='encrypted.E002'))
        return errors

    def clone(self):
        name, path, args, kwargs = super().deconstruct()
        # Determine if the class that subclassed us has been subclassed.
        if not self.__class__.__mro__.index(EncryptedMixin) > 1:
            return encrypt(self.base_class(*args, **kwargs))
        return self.__class__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Determine if the class that subclassed us has been subclassed.
        if not self.__class__.__mro__.index(EncryptedMixin) > 1:
            path = "%s.%s" % (encrypt.__module__, encrypt.__name__)
            args = [self.base_class(*args, **kwargs)]
            kwargs = {}
        return name, path, args, kwargs

    def get_internal_type(self):
        """该字段对应数据库的类型"""
        type_ = super().get_internal_type()
        if type_ not in ('TextField', 'CharField'):
            raise Exception('目前支持 char、text 类型字段')
        return type_

    def get_db_prep_value(self, value, connection, prepared=False):
        """查询前转换"""
        value = models.Field.get_db_prep_value(self, value, connection, prepared)
        if value not in self.skip_types:
            assert isinstance(value, str)
            value = self.encrypt.encrypt(value)
        return value

    def get_db_prep_save(self, value, connection):
        """入库前转换"""
        ret = super().get_db_prep_save(value, connection)
        return ret

    def from_db_value(self, value, *args, **kwargs):
        """出库前转换"""
        if value not in self.skip_types:
            return self.encrypt.decrypt(value)
        return value


class EncryptTool(object):
    # ENCRYPT_KEY = settings.ENCRYPT_KEY
    ENCRYPT_KEY = "abcdef9080"

    def translate(self, source, key):
        from itertools import cycle
        result = ''
        temp = cycle(key)
        for ch in source:
            result = result + chr(ord(ch) ^ ord(next(temp)))
        return result

    def encrypt(self, source):
        encrypt_str = self.translate(source, self.ENCRYPT_KEY)
        return encrypt_str

    def decrypt(self, source):
        decrypt_str = self.translate(source, self.ENCRYPT_KEY)
        return decrypt_str


def get_encrypted_field(base_class, skip_types):
    """
    A get or create method for encrypted fields, we cache the field in
    the module to avoid recreation. This also allows us to always return
    the same class reference for a field.

    :type base_class: models.Field[T]
    :rtype: models.Field[EncryptedMixin, T]
    """
    assert not isinstance(base_class, models.Field)
    field_name = 'Encrypted' + base_class.__name__
    if base_class not in FIELD_CACHE:
        FIELD_CACHE[base_class] = type(field_name,
                                       (EncryptedMixin, base_class), {
                                           'base_class': base_class,
                                           'skip_types': skip_types,
                                       })
    return FIELD_CACHE[base_class]


def encrypt(base_field, skip_types: typing.Iterable=None):
    """
    A decorator for creating encrypted model fields.

    :type base_field: models.Field[T]
    :param bytes key: This is an optional argument.

        Allows for specifying an instance specific encryption key.
    :param int ttl: This is an optional argument.

        The amount of time in seconds that a value can be stored for. If the
        time to live of the data has passed, it will become unreadable.
        The expired value will return an :class:`Expired` object.
    :rtype: models.Field[EncryptedMixin, T]
    """
    if not isinstance(base_field, models.Field):
        return get_encrypted_field(base_field, skip_types=skip_types)

    name, path, args, kwargs = base_field.deconstruct()
    return get_encrypted_field(type(base_field), skip_types=skip_types)(*args, **kwargs)
