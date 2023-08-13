
from django.db import models
from random import *

class account(models.Model) : 
    user_id = models.BigAutoField(help_text="User ID", primary_key=True, verbose_name="유저 아이디"),
    password = models.CharField(max_length=300, verbose_name="비밀번호")
    name = models.CharField(max_length=64, verbose_name="이름")
    email = models.EmailField(max_length=128, unique=True, verbose_name="사용자 이메일")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="생성일자")
    modifiedDate = models.DateTimeField(auto_now=True, verbose_name="수정일자")
    sex = models.BooleanField(null=True)
    birthdate = models.DateTimeField(null=True)
    nickname = models.CharField(max_length=64, unique=True, verbose_name="이름")
    profileImage = models.ImageField(null=True)
    #전화번호 인증을 위한 Column
    phone = models.CharField(max_length=15, unique=True, verbose_name= "전화번호")
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    class Meta : 
        db_table = 'Account'