from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.exceptions import ValidationError,APIException
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
import random
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password

#-------------------login---------------------
class InvalidInformationException(APIException):
    status_code = 400
    default_detail = 'Informations invalides'

class Mytoken(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # Extract the error message from the first element of the list
            return Response({
            'message': 'information invalide',
            'status':status.HTTP_400_BAD_REQUEST, 
        })
            
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        image_url = user.image.url if user.image else None
        return Response({
            'message': 'login success',
            'status':status.HTTP_200_OK, 
            'id': user.id,
            'email': user.email,
            'firstname': user.firstname,
            'lastname':user.lastname,
            'phone': user.phone,
            'username': user.username,
            'post': user.post,
            'image':image_url,
            'access': str(refresh.access_token),
            'refresh_token': str(refresh),  
        })
    
class RegisterAPI(TokenObtainPairView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get('username', None)
        password = request.data.get('password', None)

        if phone is None or password is None:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Envoyez le username et le mdp'})

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()
            user.set_password(password)
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserSerializer(user, context=self.get_serializer_context()).data,
                'token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Exception during user registration: {e}")
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Bad request'})  
        
class UpdatePassword(TokenObtainPairView):
    def put(self, request):
        phone=request.data['phone']
        password=make_password(request.data['password'])
        try:
            user=UserAub.objects.get(phone=phone)
        except:
            return Response({'message':'Ultilisateur ne existe pas'})
        user.password=password
        user.save()
        return Response({'message':'Success'})        