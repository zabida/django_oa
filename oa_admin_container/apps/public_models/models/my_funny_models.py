from django.db import models


class Person(models.Model):
    SEX_MALE = '1'
    SEX_FEMALE = '0'
    SEX_CHOICES = (
        (SEX_MALE, '男'),
        (SEX_FEMALE, '女')
    )
    name = models.CharField(max_length=12)
    age = models.CharField(max_length=3)
    sex = models.CharField(max_length=2, choices=SEX_CHOICES)
    address = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'person'
        ordering = ('-updated_at', )


class Post(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        ordering = ('-updated_at', )
