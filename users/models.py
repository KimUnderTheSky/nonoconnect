from django.db import models
from random import *
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

# 헬퍼 클래스
# class UserManager(BaseUserManager):
#     def create_user(self, email, password, **kwargs):
#         """
#         주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#         user = self.model(
#             email = email,
#         )
#         user.set_password(password)
#         user.save(using = self._db)

#         return user
    

#     def create_superuser(self, email,username, name, password):
#         """
#         주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
#         단, 최상위 사용자이므로 권한을 부여
#         """
#         superuser = self.create_user(
#             email=email,
#             password=password,
#         )

#         superuser.is_staff = True
#         superuser.superuser = True
#         superuser.is_active = True

#         superuser.save(using=self._db)
#         return superuser


class User(models.Model):
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
    
    class Meta:
        db_table = 'User'

    def AuthSave(self, *args, **kwargs):
        self.phonenumber = User.phone
        self.authnumber = randint(1000,10000)
        super().save(*args, **kwargs)
        # self.AuthSendsms()

    def make_signature(self, message):
        pass

    # def AuthSendsms(self):
    #     URL

    #입력받은 인증번호 확인
    def AuthNumCheck(phoneNum, authNum):
        result = User.objects.get(phone = phoneNum , authnumber = authNum)
        
        if result :
            return True
        return False