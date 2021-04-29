import json
import bcrypt
import jwt
import re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from my_settings import SECRET_KEY, ALGORITHM
from .utils      import login_decorator
from .models     import User

MINIMUM_PASSWORD_LENGTH = 8
MINIMUM_NAME_LENGTH     = 2
MAXIMUN_NAME_LENGTH     = 15

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data.get('email')
            password = data.get('password')                               
            name     = data.get('name')

            email_pattern = re.compile('[^@]+@[^@]+\.[^@]+')

            if not (email and password and name):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not re.match(email_pattern, email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

            if len(name) < MINIMUM_NAME_LENGTH or len(name) > MAXIMUN_NAME_LENGTH:
                return JsonResponse({'message':'INVALID_NAME'}, status=400)

            if User.objects.filter(Q(name=name) | Q(email=email)).exists():
                return JsonResponse({'message':'USER_ALREADY_EXISTS'}, status=409)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = email,
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name     = name,
            )

            return JsonResponse({'message':'SUCCESS'}, status=201)
                
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)


class SigninView(View):
    def post(self, request):
        try: 
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email = email).exists():
                return JsonResponse({'mesage' : 'INVALID_USER'}, status = 401)

            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({'message': 'SUCCESS', 'access_token': token}, status=200)
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


