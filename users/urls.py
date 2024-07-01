from django.urls import path
from .views import *

urlpatterns = [
    ####---------Login-------------#####
    path('login/', Mytoken.as_view(), name='token_obtain_pair'),
    ####---------Register-------------#####
    path('register/', RegisterAPI.as_view(), name='user-register'),
    ####---------Change Password-------------#####
    path('password/', UpdatePassword.as_view(),name='update_password'),
    ####---------Edit Profile-------------#####
    path('update-profile/<int:id>/',UserAubUpdateView.as_view(), name='user-update'),


    ###----------- cheque -------------#####
    path('send_email/<str:code_agence>/', SendEmailView.as_view(), name='send_email'),
    ###----------- cheque envoyer-------------#####
    path('cheque-envoyer/', ChequeEnvoyer.as_view(), name='cheque-envoyer'),
    ###----------- cheque envoyer-------------#####
    path('cheque-banque-envoyer/', ChequeBanqueEnvoyer.as_view(), name='cheque-banque-envoyer'),
    ###----------- cheque envoyer excel NDB ** NKTT -------------#####
    path('cheque-envoyer-excel/<str:code_agence>/', ChequeEnvoyerExcelAgence.as_view(), name='cheque-envoyer-excel-agence'),
    ###----------- cheque envoyer excel-------------#####
    path('cheque-envoyer-excel/', ChequeEnvoyerExcel.as_view(), name='cheque-envoyer-excel'),
    ###----------- cheque demander-------------#####
    path('cheque-demander/', ChequeDemander.as_view(), name='cheque-demander'),
    ###----------- tous les cheque  -------------#####
    path('all-cheque/', AllCheque.as_view(), name='cheque-all'),
    ###----------- tous les excel cheque  -------------#####
    path('all-cheque-excel/', AllChequeExcell.as_view(), name='cheque-all-excell'),
    ###----------- tous les cheques -------------####
    path('send_all_email/', SendAllChequeEmailView.as_view(), name='send_email_all'),
    ###------ archive ------###
    path('get-archive/', ArchiveListAPIView.as_view(), name='archiv-list'),
    ###------------- les table utiliser -----#####  
    path('demchq/', MyDemChqListAPIView.as_view(), name='demchq-list'),
    path('agence/', AgenceListAPIView.as_view(), name='agence-list'),
    path('client/', ClientListAPIView.as_view(), name='client-list'),
    path('DemChqDt/', DemChqDtlListAPIView.as_view(), name='DemChqDt-list'),

]
