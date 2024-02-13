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
from django.core.mail import send_mail
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
            'role': user.role,
            'access': str(refresh.access_token),
            'refresh_token': str(refresh),  
        })
    
class RegisterAPI(TokenObtainPairView):
    serializer_classes = {
        'Caissier': RegisterCaissierSerializer,
        'ChefAgence': RegisterChefAgenceSerializer
    }

    def get_serializer_class(self):
        role = self.request.data.get('role', False)
        serializer_class = self.serializer_classes.get(role)
        return serializer_class

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        role = request.data.get('role', False)

        if phone and password and role:
            serializer_class = self.get_serializer_class()
            if serializer_class is None:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Invalid role'})

            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                user = serializer.save()
                user.set_password(password)
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'phone':user.phone,
                    'username':user.username,
                    'email':user.email,
                    'post':user.post,
                    'role': user.role,
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            except:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Bad request'})

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Envoyez le numéro de telephone exist'})


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
    

class SendEmailView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            job = serializer.validated_data['job']
            # Send email
            subject = 'New Job Application'
            message = f'Name: {name}\nJob: {job}'
            recipient_list = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class getChequeView(APIView):
    def get(self, request):
        # Récupérez tous les documents
        demchq = cheque.objects.all()
        serializer = chequeSerializer(demchq, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)      