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
from django.core.mail import send_mail,EmailMessage
from django.db.models import ExpressionWrapper
from django.db.models import F
from django.db.models import IntegerField
from django.db.models import Value

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
            subj = serializer.validated_data['subj']
            file = serializer.validated_data['file']

            try:
                # Attach the file to the email
                email = EmailMessage(
                    subject='Nouveau Cheque',
                    body=f'Name: {name}\nSubject: {subj}',
                    from_email=settings.EMAIL_HOST_USER,
                    to=['killermbare@gmail.com']  # Set the receiver email here
                )
                
                # Read the file content
                file_content = file.read()

                # Attach the file to the email
                email.attach(file.name, file_content, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

                # Send the email
                email.send()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class getChequeView(APIView):
    def get(self, request):
        # Récupérez tous les documents
        demchq = cheque.objects.all()
        serializer = chequeSerializer(demchq, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)      

class AgenceListAPIView(APIView):
    def get(self, request):
        # Récupérez tous les documents
        agence = Agence.objects.all()
        serializer = AgenceSerializer(agence, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   

class ClientListAPIView(APIView):
    def get(self, request):
        # Récupérez tous les documents
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     

class DemChqDtlListAPIView(APIView):
    def get(self, request):
        # Récupérez tous les documents
        demChqDtl = DemChqDtl.objects.all()
        serializer = DemChqDtlSerializer(demChqDtl, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)                
        
class MyDemChqListAPIView(generics.ListAPIView):
    serializer_class = DemChqSerializer

    def get_queryset(self):
        return DemChq.objects.exclude(DATVALID__isnull=True)

        

##les cheques envoyer 
class chequeEnvoyer(APIView):
    def get(self, request):
        # Récupérer les objets DemChq avec DATVALID non nul
        dem_chqs = DemChq.objects.filter(DATVALID__isnull=False)

        # Initialiser une liste pour stocker les résultats
        results = []

        # Boucler à travers les objets DemChq
        for dem_chq in dem_chqs:
            # Filtrer les objets DemChqDtl en fonction de l'objet DemChq actuel
            dem_chqsdt = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER).first()
            
            # Vérifier si un objet DemChqDtl a été trouvé
            if dem_chqsdt:
                # Récupérer les valeurs de REFER1 et REFER2
                refer1 = dem_chqsdt.REFER1
                refer2 = dem_chqsdt.REFER2

                # Calculer nbre_feuiles
                nbre_feuiles = int(refer2) - int(refer1) + 1

                # Créer un dictionnaire pour stocker les résultats
                result = {
                    'Nligne': dem_chq.id,
                    'numero de compte': dem_chq.COMPTE,
                    'code agence': dem_chq.CLIENT.CODE_AGENCE,
                    'nbrchq': dem_chq.NBRCHQ,
                    'nbre_feuiles': nbre_feuiles,
                    'code_transaction': 1,  # Vous avez défini 1 comme valeur fixe
                    'nom de client':dem_chq.CLIENT.NOM,
                    'addresse': dem_chq.ADRL2,
                    'code devise': 929,
                    'code bank': 26,
                    'code pays': 2,
                    'numero de debut': refer1,
                }

                # Ajouter le dictionnaire à la liste des résultats
                results.append(result)

        # Retourner les résultats en tant que réponse JSON
        return Response(results)