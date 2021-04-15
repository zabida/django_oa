# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': '123456',
        'NAME': 'oa_admin',
        'HOST': '8.129.121.170',
        'PORT': '13307',
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
    }
}


# Cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://8.129.121.170:5002/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
