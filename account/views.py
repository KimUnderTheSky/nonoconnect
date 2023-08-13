

import json, re
from json.decoder import JSONDecodeError
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

from account.models import *
from django.shortcuts import redirect

# Create your views here.

PASSWORD_MIN_LEN = 8

class account_Signup(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)

            print(data)

            nickname = data.get('nickname', None)
            name = data.get('name',None)
            password = data.get('password',None)
            phone = data.get('phone', None)
            email = data.get('email', None)
            # createdDate = data.get('createdDate', None)
            # modifiedDate = data.get('modifiedDate', None)

            print(nickname)
            print(name)
            print(password)
            print(phone)
            print(email)
            # print(createdDate)
            # print(modifiedDate)

            # email / 전화번호 / 닉네임 
            email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')
            phone_number_pattern = re.compile('^[0-9]{1,15}$')

            if not (
                email
                and password
                and nickname
                and phone
            ):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            #email 양식에 맞게 입력되었는가
            if email:
                if not re.match(email_pattern, email):
                    return JsonResponse ({'message':'EMAIL_VALIDATION_ERROR'}, status = 400)
            
            #전화번호 양식에 맞게 입력되었는가
            if phone:
                if not re.match(phone_number_pattern, phone):
                    return JsonResponse ({'message':'PHONE_NUMBER_VALIDATION_ERROR'}, status = 400)

            #비밀번호 최소 길이
            if len(password) < PASSWORD_MIN_LEN :
                return JsonResponse({'message' : 'PASSWORD_VALIDATION_ERROR'}, status = 400)

            #계정 존재 여부
            if account.objects.filter(
                Q(email = data['email']) &
                Q(phone = data['phone']) &
                Q(nickname = data['nickname'])
            ).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 400)
            #비밀번호 암호화
            encrypted_password = make_password(password)
            account.objects.create(
                nickname = nickname,
                password = encrypted_password,
                name = name,
                email = email,
                phone = phone,
                # createdDate = createdDate,
                # modifiedDate = modifiedDate,
                sex = True,
                # birthDate = datetime.now(),
                profileImage = None,
                latitude = 0.0,
                longitude = 0.0 
            )
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status = 400)

class account_Login(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)

            login_id = data.get('nickname', None)
            login_password = data.get('password', None)

            if not (
                login_id
                and login_password
            ):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            
            if not account.objects.filter(nickname = login_id).exists : 
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            user = account.objects.get(nickname = login_id)

            if check_password(login_password, user.password):
                # 인증 성공
                print("로그인 성공")
                request.session['user_id'] = user.id
                return redirect('/')
            else:
                # 인증 실패
                return JsonResponse({'message': 'Login failed'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
