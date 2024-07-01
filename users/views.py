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
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
import requests
import json
from django.db.models import Q
import logging



class UserAubUpdateView(generics.UpdateAPIView):
    queryset = UserAub.objects.all()
    serializer_class = UserAubSerializer
    lookup_field = 'id'
    
    def get_object(self):
        user_id = self.kwargs.get('id')
        return generics.get_object_or_404(UserAub, id=user_id)

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
            'code_agence':user.code_agence,
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
                    'code_agence':user.code_agence,
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
    
#----------- envoye du cheque -----------
logger = logging.getLogger(__name__)
def format_refer1(refer1):
    if len(refer1) == 1:
        return '000000' + refer1
    elif len(refer1) == 2:
        return '00000' + refer1
    elif len(refer1) == 3:
        return '0000' + refer1
    elif len(refer1) == 4:
        return '000' + refer1
    elif len(refer1) == 5:
        return '00' + refer1
    elif len(refer1) == 6:
        return '0' + refer1
    else:
        return refer1



logger = logging.getLogger(__name__)

class SendEmailView(APIView):
    def post(self, request, code_agence):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            subj = serializer.validated_data['subj']
            file = serializer.validated_data['file']

            try:
                # Attach the file to the email
                email = EmailMessage(
                    subject='Personalisation Chequier',
                    body=f'\nBonjour \nMerci de trouver ci-joint les fichiers de personnalisation des chéquiers, formaté selon vos spécifications \nBien Cordialement',
                    from_email=settings.EMAIL_HOST_USER,
                    #to=['secure_mauritanie@secureprinte.com']  # Set the receiver email here Production
                    to=['killermbare@gmail.com'] # Set the receiver email here test
                    
                )
                
                # Read the file content
                file_content = file.read()

                # Attach the file to the email
                email.attach(file.name, file_content, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

                # Send the email
                email.send()

                # URL de l'API à consommer
                api_url = f"http://127.0.0.1:8000/users/cheque-envoyer-excel/{code_agence}/"

                # Récupérer les données du corps de la requête
                body_data = {
                    'name': name,
                    'subj': subj,
                    # Exclure le fichier des données
                }

                try:
                    logger.info("Sending email and making API request")
                    logger.info(f"API URL: {api_url}")
                    logger.info(f"Body data: {body_data}")

                    # Envoyer une requête GET à l'API avec les données du corps et le fichier
                    response = requests.get(api_url, data=body_data, files={'file': file})
                    
                    # Vérifier si la requête a réussi en vérifiant le code de statut de la réponse
                    if response.status_code == 200:
                        # Extraire les données de la réponse de l'API
                        api_data = response.json()  # Convertir la réponse en JSON
                        # Créer un nouvel objet Archive avec les données extraites
                        # Parcourir la liste de dictionnaires dans la réponse
                        for data in api_data:
                            # Créer un nouvel objet Archive avec les données de chaque dictionnaire

                            archive_data = {
                                'numero_de_compte': data['numero de compte'],
                                'code_agence': data['code agence'],
                                'nbrchq': data['Nbre carnet'],
                                'nbre_feuiles': data['Nbre feuilles'],
                                'code_transaction': data['code transaction'],
                                'nom_de_client': data['nom client'],
                                'addresse': data['adresse'],
                                'status': data.get('status', ''),  # Vérifier si 'status' existe
                                'code_devise': data['Code Devise'],
                                'code_bank': data['code bank'],
                                'code_pays': data['code pays'],
                                'numero_de_debut': data['numero de debut'],
                            }

                            # Créer un objet Archive
                            Archive.objects.create(**archive_data)
                        # La requête a réussi, renvoyer un message de succès avec un statut OK
                        return Response({"status": "Success", "message": "Le demande Cheque a été envoyée et Archive avec succès."}, status=status.HTTP_200_OK)
                    else:
                        # La requête a échoué ou le contenu de la réponse ne correspond pas à ce qui est attendu
                        return Response({"status": "Error", "message": f"La requête à l'API a échoué avec le code de statut {response.status_code}."}, status=response.status_code)
                except Exception as e:
                    # Une erreur s'est produite lors de la tentative de consommation de l'API
                    logger.error(f"Error while making API request: {str(e)}")
                    return Response({"status": "Error", "message": f"Une erreur s'est produite : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
            except Exception as e:
                logger.error(f"Error while sending email: {str(e)}")
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

        

##------- les cheques envoyer --------
class ChequeEnvoyer(APIView):
    def get(self, request):
        # Récupérer les objets DemChq avec DATVALID non nul
        dem_chqs = DemChq.objects.filter(DATEDDEM__isnull=False,DATREMCL__isnull=True).exclude(CLIENT='218009')

        # Initialiser une liste pour stocker les résultats
        results = []

        # Boucler à travers les objets DemChq
        for dem_chq in dem_chqs:
            # Filtrer les objets DemChqDtl en fonction de l'objet DemChq actuel
            dem_chqsdt = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER,STATUS='ST').first()
            
            # Vérifier si un objet DemChqDtl a été trouvé
            if dem_chqsdt:
                # Récupérer les valeurs de REFER1 et REFER2
                refer1 = dem_chqsdt.REFER1
                refer2 = dem_chqsdt.REFER2
                status = dem_chqsdt.STATUS 
                # Calculer nbre_feuiles
                nbre_feuiles = int(refer2) - int(refer1) + 1

                # Créer un dictionnaire pour stocker les résultats
                result = {
                    'numero_de_compte': dem_chq.COMPTE,
                    'code_agence': dem_chq.CLIENT.CODE_AGENCE,
                    'nbrchq': dem_chq.NBRCHQ,
                    'nbre_feuiles': nbre_feuiles,
                    'code_transaction': 1,  
                    'nom_de_client': dem_chq.CLIENT.NOM,
                    'addresse': dem_chq.ADRL2,
                    'status': dem_chqsdt.STATUS,
                    'code_devise': 929,
                    'code_bank': '00026',
                    'code_pays': str('02'),
                    'numero_de_debut': format_refer1(refer1),
                }

                # Ajouter le dictionnaire à la liste des résultats
                results.append(result)

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 16
        paginated_results = paginator.paginate_queryset(results, request)

        # Retourner les résultats paginés en tant que réponse JSON
        return paginator.get_paginated_response(paginated_results)


##------- les cheques de banque envoyer --------
class ChequeBanqueEnvoyer(APIView):
    def get(self, request):
        # Récupérer les objets DemChq avec DATVALID non nul
        dem_chqs = DemChq.objects.filter(DATEDDEM__isnull=False,DATREMCL__isnull=True,CLIENT='218009')

        # Initialiser une liste pour stocker les résultats
        results = []

        # Boucler à travers les objets DemChq
        for dem_chq in dem_chqs:
            # Filtrer les objets DemChqDtl en fonction de l'objet DemChq actuel
            dem_chqsdt = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER,STATUS='ST').first()
            
            # Vérifier si un objet DemChqDtl a été trouvé
            if dem_chqsdt:
                # Récupérer les valeurs de REFER1 et REFER2
                refer1 = dem_chqsdt.REFER1
                refer2 = dem_chqsdt.REFER2
                status = dem_chqsdt.STATUS 
                # Calculer nbre_feuiles
                nbre_feuiles = int(refer2) - int(refer1) + 1

                # Créer un dictionnaire pour stocker les résultats
                result = {
                    'numero_de_compte': dem_chq.COMPTE,
                    'code_agence': dem_chq.CLIENT.CODE_AGENCE,
                    'nbrchq': dem_chq.NBRCHQ,
                    'nbre_feuiles': nbre_feuiles,
                    'code_transaction': 1,  
                    'nom_de_client': dem_chq.CLIENT.NOM,
                    'addresse': dem_chq.ADRL2,
                    'status': dem_chqsdt.STATUS,
                    'code_devise': 929,
                    'code_bank': '00026',
                    'code_pays': str('02'),
                    'numero_de_debut': format_refer1(refer1),
                }

                # Ajouter le dictionnaire à la liste des résultats
                results.append(result)

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 16
        paginated_results = paginator.paginate_queryset(results, request)

        # Retourner les résultats paginés en tant que réponse JSON
        return paginator.get_paginated_response(paginated_results)

##------- all cheque aub -------
class AllCheque(APIView):
    def get(self, request):
        # Récupérer les objets DemChq avec DATVALID non nul
        dem_chqs = DemChq.objects.filter()

        # Initialiser une liste pour stocker les résultats
        results = []

        # Boucler à travers les objets DemChq
        for dem_chq in dem_chqs:
            # Filtrer les objets DemChqDtl en fonction de l'objet DemChq actuel
            dem_chqsdt = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER).filter(Q(STATUS='RQ') | Q(STATUS='ST') | Q(STATUS='RE') | Q(STATUS='DS')| Q(STATUS='DT')).first()
         
            # Vérifier si un objet DemChqDtl a été trouvé
            if dem_chqsdt:
                # Récupérer les valeurs de REFER1 et REFER2
                refer1 = dem_chqsdt.REFER1
                refer2 = dem_chqsdt.REFER2
                status = dem_chqsdt.STATUS 
                # Calculer nbre_feuiles
                nbre_feuiles = int(refer2) - int(refer1) + 1

                # Créer un dictionnaire pour stocker les résultats
                result = {
                    'numero_de_compte': dem_chq.COMPTE,
                    'code_agence': dem_chq.CLIENT.CODE_AGENCE,
                    'nbrchq': dem_chq.NBRCHQ,
                    'nbre_feuiles': nbre_feuiles,
                    'code_transaction': 1,  
                    'nom_de_client': dem_chq.CLIENT.NOM,
                    'addresse': dem_chq.ADRL2,
                    'status': dem_chqsdt.STATUS,
                    'code_devise': 929,
                    'code_bank': '00026',
                    'code_pays': str('02'),
                    'numero_de_debut': format_refer1(refer1) ,
                }

                # Ajouter le dictionnaire à la liste des résultats
                results.append(result)

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 16
        paginated_results = paginator.paginate_queryset(results, request)

        # Retourner les résultats paginés en tant que réponse JSON
        return paginator.get_paginated_response(paginated_results)

##------- all cheque aub excel -------
class AllChequeExcell(APIView):
    def get(self, request):
        # Récupérer les objets DemChq avec DATVALID non nul
        dem_chqs = DemChq.objects.filter()

        # Initialiser une liste pour stocker les résultats
        results = []

        # Boucler à travers les objets DemChq
        for dem_chq in dem_chqs:
            # Filtrer les objets DemChqDtl en fonction de l'objet DemChq actuel
            dem_chqsdt = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER).filter(Q(STATUS='RQ') | Q(STATUS='ST') | Q(STATUS='RE') | Q(STATUS='DS')| Q(STATUS='DT')).first()
         
            # Vérifier si un objet DemChqDtl a été trouvé
            if dem_chqsdt:
                # Récupérer les valeurs de REFER1 et REFER2
                refer1 = dem_chqsdt.REFER1
                refer2 = dem_chqsdt.REFER2
                status = dem_chqsdt.STATUS 
                # Calculer nbre_feuiles
                nbre_feuiles = int(refer2) - int(refer1) + 1

                # Créer un dictionnaire pour stocker les résultats
                result = {
                    'numero_de_compte': dem_chq.COMPTE,
                    'code_agence': dem_chq.CLIENT.CODE_AGENCE,
                    'nbrchq': dem_chq.NBRCHQ,
                    'nbre_feuiles': nbre_feuiles,
                    'code_transaction': 1,  
                    'nom_de_client': dem_chq.CLIENT.NOM,
                    'addresse': dem_chq.ADRL2,
                    'status': dem_chqsdt.STATUS,
                    'code_devise': 929,
                    'code_bank': '00026',
                    'code_pays': str('02'),
                    'numero_de_debut': format_refer1(refer1) ,
                }

                # Ajouter le dictionnaire à la liste des résultats
                results.append(result)

        return Response(results)
# ------- envoye tous les cheque ------
class SendAllChequeEmailView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            subj = serializer.validated_data['subj']
            file = serializer.validated_data['file']


            try:
                # Attach the file to the email
                email = EmailMessage(
                    subject=' Cheque',
                    body=f'\n{subj}',
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
##------- les cheques Demander --------
class ChequeDemander(APIView):
    def get(self, request):
        # Récupérer les objets DemChq avec DATVALID non nul
        dem_chqs = DemChq.objects.filter(DATDEM__isnull=False,DATREMCL__isnull=True)

        # Initialiser une liste pour stocker les résultats
        results = []

        # Boucler à travers les objets DemChq
        for dem_chq in dem_chqs:
            # Filtrer les objets DemChqDtl en fonction de l'objet DemChq actuel
            dem_chqsdt = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER,STATUS='RQ').first()
            
            # Vérifier si un objet DemChqDtl a été trouvé
            if dem_chqsdt:
                # Récupérer les valeurs de REFER1 et REFER2
                refer1 = dem_chqsdt.REFER1
                refer2 = dem_chqsdt.REFER2
                status = dem_chqsdt.STATUS 
                # Calculer nbre_feuiles
                nbre_feuiles = int(refer2) - int(refer1) + 1

                # Créer un dictionnaire pour stocker les résultats
                result = {
                    'numero_de_compte': dem_chq.COMPTE,
                    'code_agence': dem_chq.CLIENT.CODE_AGENCE,
                    'nbrchq': dem_chq.NBRCHQ,
                    'nbre_feuiles': nbre_feuiles,
                    'code_transaction': 1,  
                    'nom_de_client': dem_chq.CLIENT.NOM,
                    'addresse': dem_chq.ADRL2,
                    'status': dem_chqsdt.STATUS,
                    'code_devise': 929,
                    'code_bank': '00026',
                    'code_pays': str('02'),
                    'numero_de_debut': format_refer1(refer1) ,
                }

                # Ajouter le dictionnaire à la liste des résultats
                results.append(result)

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 16
        paginated_results = paginator.paginate_queryset(results, request)

        # Retourner les résultats paginés en tant que réponse JSON
        return paginator.get_paginated_response(paginated_results)


#------ generer un fichier excel NDB ** NKTT--------
class ChequeEnvoyerExcelAgence(APIView):
    def get(self, request,code_agence):
        # Retrieve DemChq objects with non-null DATVALID and null DATREMCL
        dem_chqs = DemChq.objects.filter(DATEDDEM__isnull=False, DATREMCL__isnull=True,CLIENT__CODE_AGENCE=code_agence)

        # Initialize a list to store the results
        results = []

        # URL of the API to fetch existing archives
        api_url = "http://127.0.0.1:8000/users/get-archive/"

        try:
            # Send a GET request to the API to fetch existing archives
            response = requests.get(api_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract data from the response
                archive_data = response.json()

                # Loop through the DemChq objects
                for dem_chq in dem_chqs:
                    # Filter DemChqDtl objects based on the current DemChq object
                    dem_chq_dtl = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER, STATUS='ST').first()

                    if dem_chq_dtl:
                        # Retrieve the REFER1 and REFER2 values
                        refer1 = dem_chq_dtl.REFER1
                        refer2 = dem_chq_dtl.REFER2

                        # Calculate nbre_feuiles
                        nbre_feuiles = int(refer2) - int(refer1) + 1

                        # Check if these data already exist in the archives


                        if not any(
                            archive['numero_de_compte'] == dem_chq.COMPTE and
                            archive['code_agence'] == dem_chq.CLIENT.CODE_AGENCE and
                            archive['nbrchq'] == dem_chq.NBRCHQ and
                            archive['nbre_feuiles'] == nbre_feuiles and
                            archive['code_transaction'] == 1 and
                            archive['nom_de_client'] == dem_chq.CLIENT.NOM and
                            archive['addresse'] == dem_chq.ADRL2 and
                            archive['code_devise'] == 929 and
                            archive['code_bank'] == '00026' and
                            archive['code_pays'] == '02' and
                            archive['numero_de_debut'] == format_refer1(refer1)   
                            for archive in archive_data
                        ):
                            # If the data do not exist, add them to the results list
                            result = {
                                'numero de compte': dem_chq.COMPTE,
                                'code agence': dem_chq.CLIENT.CODE_AGENCE,
                                'Nbre carnet': dem_chq.NBRCHQ,
                                'Nbre feuilles': nbre_feuiles,
                                'code transaction': 1,
                                'nom client': dem_chq.CLIENT.NOM,
                                'adresse': dem_chq.ADRL2,
                                'Code Devise': 929,
                                'code bank': '00026',
                                'code pays': '02',
                                'numero de debut': format_refer1(refer1),
                            }
                            results.append(result)

                # Return the results as a JSON response
                return Response(results, status=status.HTTP_200_OK)

            else:
                # The request failed
                return Response({"status": "Error", "message": f"La requête à l'API a échoué avec le code de statut {response.status_code}."}, status=response.status_code)

        except Exception as e:
            # An error occurred during the API request
            logger.error(f"Error while making API request: {str(e)}")
            return Response({"status": "Error", "message": f"Une erreur s'est produite : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#------ generer un fichier excel -------
class ChequeEnvoyerExcel(APIView):
    def get(self, request):
        # Retrieve DemChq objects with non-null DATVALID and null DATREMCL
        dem_chqs = DemChq.objects.filter(DATEDDEM__isnull=False, DATREMCL__isnull=True)

        # Initialize a list to store the results
        results = []

        # URL of the API to fetch existing archives
        api_url = "http://127.0.0.1:8000/users/get-archive/"

        try:
            # Send a GET request to the API to fetch existing archives
            response = requests.get(api_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract data from the response
                archive_data = response.json()

                # Loop through the DemChq objects
                for dem_chq in dem_chqs:
                    # Filter DemChqDtl objects based on the current DemChq object
                    dem_chq_dtl = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER, STATUS='ST').first()

                    if dem_chq_dtl:
                        # Retrieve the REFER1 and REFER2 values
                        refer1 = dem_chq_dtl.REFER1
                        refer2 = dem_chq_dtl.REFER2

                        # Calculate nbre_feuiles
                        nbre_feuiles = int(refer2) - int(refer1) + 1

                        # Check if these data already exist in the archives
                        if not any(
                            archive['numero_de_compte'] == dem_chq.COMPTE and
                            archive['code_agence'] == dem_chq.CLIENT.CODE_AGENCE and
                            archive['nbrchq'] == dem_chq.NBRCHQ and
                            archive['nbre_feuiles'] == nbre_feuiles and
                            archive['code_transaction'] == 1 and
                            archive['nom_de_client'] == dem_chq.CLIENT.NOM and
                            archive['addresse'] == dem_chq.ADRL2 and
                            archive['code_devise'] == 929 and
                            archive['code_bank'] == '00026' and
                            archive['code_pays'] == '02' and
                            archive['numero_de_debut'] == format_refer1(refer1)   
                            for archive in archive_data
                        ):
                            # If the data do not exist, add them to the results list
                            result = {
                                'numero_de_compte': dem_chq.COMPTE,
                                'code_agence': dem_chq.CLIENT.CODE_AGENCE,
                                'nbrchq': dem_chq.NBRCHQ,
                                'nbre_feuiles': nbre_feuiles,
                                'code_transaction': 1,
                                'nom_de_client': dem_chq.CLIENT.NOM,
                                'addresse': dem_chq.ADRL2,
                                'code_devise': 929,
                                'code_bank': '00026',
                                'code_pays': '02',
                                'numero_de_debut': format_refer1(refer1),
                            }
                            results.append(result)

                # Return the results as a JSON response
                return Response(results, status=status.HTTP_200_OK)

            else:
                # The request failed
                return Response({"status": "Error", "message": f"La requête à l'API a échoué avec le code de statut {response.status_code}."}, status=response.status_code)

        except Exception as e:
            # An error occurred during the API request
            logger.error(f"Error while making API request: {str(e)}")
            return Response({"status": "Error", "message": f"Une erreur s'est produite : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ArchiveListAPIView(generics.ListAPIView):
    def get(self, request):
        # Récupérez tous les documents
        archive = Archive.objects.all()
        serializer = ArchiveSerializer(archive, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        

# ------ cheque de banque --------       
class ChequeEnvoyer(APIView):
    def get(self, request):
        # Récupérer les objets DemChq avec DATVALID non nul
        dem_chqs = DemChq.objects.filter(DATEDDEM__isnull=False,DATREMCL__isnull=True)

        # Initialiser une liste pour stocker les résultats
        results = []

        # Boucler à travers les objets DemChq
        for dem_chq in dem_chqs:
            # Filtrer les objets DemChqDtl en fonction de l'objet DemChq actuel
            dem_chqsdt = DemChqDtl.objects.filter(CHECKBK_NOOPER=dem_chq.NOOPER,STATUS='ST').first()
            
            # Vérifier si un objet DemChqDtl a été trouvé
            if dem_chqsdt:
                # Récupérer les valeurs de REFER1 et REFER2
                refer1 = dem_chqsdt.REFER1
                refer2 = dem_chqsdt.REFER2
                status = dem_chqsdt.STATUS 
                # Calculer nbre_feuiles
                nbre_feuiles = int(refer2) - int(refer1) + 1

                # Créer un dictionnaire pour stocker les résultats
                result = {
                    'numero_de_compte': dem_chq.COMPTE,
                    'code_agence': dem_chq.CLIENT.CODE_AGENCE,
                    'nbrchq': dem_chq.NBRCHQ,
                    'nbre_feuiles': nbre_feuiles,
                    'code_transaction': 1,  
                    'nom_de_client': dem_chq.CLIENT.NOM,
                    'addresse': dem_chq.ADRL2,
                    'status': dem_chqsdt.STATUS,
                    'code_devise': 929,
                    'code_bank': '00026',
                    'code_pays': str('02'),
                    'numero_de_debut': format_refer1(refer1),
                }

                # Ajouter le dictionnaire à la liste des résultats
                results.append(result)

        # Pagination des résultats
        paginator = PageNumberPagination()
        paginator.page_size = 16
        paginated_results = paginator.paginate_queryset(results, request)

        # Retourner les résultats paginés en tant que réponse JSON
        return paginator.get_paginated_response(paginated_results)