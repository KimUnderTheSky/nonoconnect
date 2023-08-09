import hmac, base64, hashlib, time , requests , json


from django.db import models
from random import *
from my_settings import *
from django.http import HttpResponse

class User(models.Model):
    password = models.CharField(max_length=300, blank= False, verbose_name="비밀번호")
    name = models.CharField(max_length=64, verbose_name="이름")
    email = models.EmailField(max_length=128, unique=True, verbose_name="사용자 이메일")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="생성일자")
    modifiedDate = models.DateTimeField(auto_now=True, verbose_name="수정일자")
    sex = models.BooleanField()
    birthdate = models.DateTimeField()
    nickname = models.CharField(max_length=64, blank= False, unique=True, verbose_name="이름(ID)")
    profileImage = models.ImageField()
    latitude = models.FloatField()
    longitude = models.FloatField()


    #전화번호 인증을 위한 Column
    phone = models.CharField(max_length=15, blank= False, unique=True, verbose_name= "전화번호")
    authnumber = models.IntegerField(verbose_name='인증번호')\
    
    class meta:
        db_table = 'User'

    def AuthSave(self, *args, **kwargs):
        self.authnumber = randint(1000,10000)
        super().save(*args, **kwargs)
        self.AuthSendsms()

    def make_signature(self):
        secret_key = SECRET_KEY
        secret_key = bytes(str(secret_key), 'UTF-8')

        URI = "/sms/v2/services/ncp:sms:kr:313062637980:nonoconnect/messages"
        # uri 중간에 Console - Project - 해당 Project 서비스 ID 입력 (예시 = ncp:sms:kr:263092132141:sms)
        API_URL = "http://"

        message = "POST" + " " + "URI" + "\n" + str(int(time.time() * 1000)) + "\n" + str(ACCESS_KEY)
        message = bytes(message, "UTF-8")

        signingKey = base64.b64encode(
            hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
        )

        return signingKey

    def AuthSendsms(self):
        SMS_URL = 'https://sens.apigw.ntruss.com/sms/v2/services/' + f'{SERVICEE_ID}' + '/messages'


        headers = {
            'Content-Type': "application/json; charset=UTF-8", # 네이버 참고서 차용
            'x-ncp-apigw-timestamp': str(int(time.time() * 1000)), # 네이버 API 서버와 5분이상 시간차이 발생시 오류
            'x-ncp-iam-access-key': ACCESS_KEY,
            'x-ncp-apigw-signature-v2': self.make_signature() # utils.py 이용
        }

        body = {
            "type": "SMS", 
            "contentType": "COMM",
            "from": CALLING_NUM, # 사전에 등록해놓은 발신용 번호 입력, 타 번호 입력시 오류
            "content": f"[인증번호:{self.authnumber}]", # 메세지를 이쁘게 꾸며보자
            "messages": [{"to": f"{self.phonenumber}"}] # 네이버 양식에 따른 messages.to 입력
        }

        request = requests.post(SMS_URL, data = json.dump(body), headers=headers)

        return HttpResponse(request.status_code)

    @classmethod
    #입력받은 인증번호 확인
    def AuthNumCheck(cls, phoneNum, authNum):
        result = cls.objects.get(phone = phoneNum , authnumber = authNum)
        
        if result :
            return True
        return False