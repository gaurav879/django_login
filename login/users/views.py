from os import name
from django.http import response
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from django.shortcuts import render
import jwt,datetime
import json


class RegisterView(APIView):
    def post(self,request):
        # print(request.body)
        var=json.loads(request.body)
        serializer = UserSerializer(data=var)
        serializer.is_valid(raise_exception=True)
        # print(request.body)
        serializer.save()
        # print(serializer.data)
        return Response(serializer.data)
    def get(self,request):
        return Response("****")
    
class LoginView(APIView):
    def post(self,request):
        var=json.loads(request.body)
        email= var['email']
        password= var['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed('Wrong Password!!!!!!!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.data = {
            'jwt': token
        }

        print(response)
        response.set_cookie('jwt',token)
        # print(response.cookies)
        return response

class UserView(APIView):

    def post(self, request):
        var=json.loads(request.body)

        print(var)
        encoded_jwt = var['jwt']
        print(encoded_jwt)
        if not encoded_jwt:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
            # {'some': 'payload'}
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
