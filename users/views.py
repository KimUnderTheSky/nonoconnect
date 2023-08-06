import json, re , bcrypt, jwt


from json.decoder import JSONDecodeError
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from rest_framework.views import APIView

from my_settings import SECRET, ALGORITHM
from users.models import *

# from django.shortcuts import render
# from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.

PASSWORD_MIN_LEN = 8


class SignUp(View):
    def post(self, request):
        try :
            data = json.loads(request.body)

            password = data.get('password', None)
            name = data.get('name', None)
            email = data.get('email', None)
            createDate = data.get('createDate', None)
            modifiedDate = data.get('modifiedDate', None)
            sex = data.get('sex', None)
            birthDate = data.get('birthDate', None)
            nickname = data.get('nickname', None)
            profileImage = data.get('profileImage', None)
            phone = data.get('phone', None)
            latitude = data.get('latitude', None)
            longitude = data.get('longitude', None)

            # email / 전화번호 / 닉네임 
            email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')
            phone_number_pattern = re.compile('^[0-9]{1,15}$')
            nickname_pattern      = re.compile('^(?=.*[a-z])[a-z0-9_.]+$')

            # regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
            # regex_password = '\S{8,25}'


            if not (
                email
                and password
                and nickname
                and phone
            ):
                return JsonResponse ({'message':'KEY_ERROR'}, status = 400)
            
            #email 양식에 맞게 입력되었는가
            if email:
                if not re.match(email_pattern, email):
                    return JsonResponse ({'message':'EMAIL_VALIDATION_ERROR'}, status = 400)
            
            #전화번호 양식에 맞게 입력되었는가
            if phone:
                if not re.match(phone_number_pattern, phone):
                    return JsonResponse ({'message':'PHONE_NUMBER_VALIDATION_ERROR'}, status = 400)

            #닉네임 양식에 맞게 입력되었는가
            if not re.match(nickname_pattern, name):
                return JsonResponse ({'message':'NAME_VALIDATION_ERROR'}, status = 400)
            
            #비밀번호 최소 길이
            if len(data['password']) < PASSWORD_MIN_LEN :
                return JsonResponse({'message' : 'PASSWORD_VALIDATION_ERROR'}, status = 400)

            #계정 존재 여부
            if User.objects.filter(email = data.get("email", None)).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 400)


            User.objects.create(
                password = bcrypt.hashpw(password.encode('UTF-8'),bcrypt.gensalt()).decode('utf-8'),
                name = name,
                email = email,
                createDate = createDate,
                modifiedDate = modifiedDate,
                sex = sex,
                birthDate = birthDate,
                nickname = nickname,
                profileImage = profileImage,
                phone = phone,
                latitude = latitude,
                longitude = longitude

            )

            return JsonResponse({'message' : 'SUCCESS'}, statuts = 201)


        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)
    def patch(self, request):
        pass


class LogIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user_id = data.get('id', None)
            password = data.get('password', None)


            if not (
                user_id
                and password
            ):
                return JsonResponse ({'message':'KEY_ERROR'}, status = 400)
            

            user = User.objects.get(nickname = id)

            if not bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
            
            access_token = jwt.encode({"id":user.id}, SECRET, algorithm=ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS', 'Authorization': access_token}, status = 200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

class Logout(View) :
    pass

# def login_view(request):
#     if request.method == "POST":
#         print(request.POST)

#     return render(request, "")

# def logout_view(request) :
#     logout(request)
#     return redirect("")


#비밀번호찾기
class FindPassword():
    def get(self, request):
        phone_num = request.query_params["phone"]

        if User.objects.filter(phone = phone_num).exists():
            user_profile = User.objects.get(phone = phone_num)

    def patch(self, request) :
        new_Password = request.data.get("new_password")

        try :
            user = User.objects.get()
            user.set_password()
            
        except KeyError:
            return JsonResponse ({'message':'KEY_ERROR'}, status = 400)
        

# 전화번호 인증
class SmsAuth(APIView):
    def post(self, request):
        try:
            phoneNumber = request.data.get("phone_num")

        except KeyError:
            return JsonResponse ({'message':'KEY_ERROR'}, status = 400)
        else :
            AuthSMS.objects.update_or_create(phoneNumber = phoneNumber)
            return