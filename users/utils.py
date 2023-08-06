import jwt, json

from django.http    import JsonResponse
from my_settings    import SECRET_KEY, ALGORITHM
from .models    import User

def TokenCheck(func):
    def wrapper(self, request, *args, **kwargs) : 
        try:
            access_token = request.headers.get('Authoriation')
            payload = jwt.decode(access_token, SECRET_KEY, algorithms= ALGORITHM)
            user = User.objects.get(id = payload['id'])
            request.user = user
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
        
        return func(self, request, *args, **kwargs)