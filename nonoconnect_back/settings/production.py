# 운영 환경
from .base import *
from my_settings import SECRET, ALGORITHM, MYSQL_DATABASE, MYSQL_USERNAME, MYSQL_PASSWORD
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"] # 도메인, ip

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DATABASE,
        'USER': MYSQL_USERNAME,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': 'localhost',  # 또는 MySQL 서버의 호스트
        'PORT': '3306',       # 또는 MySQL 포트 (기본값은 3306)
    }
}