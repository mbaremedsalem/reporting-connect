from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Mytoken.as_view(), name='token_obtain_pair'),
    path('register/', RegisterAPI.as_view(), name='user-register'),
    path('password/', UpdatePassword.as_view(),name='update_password'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send_email/', SendEmailView.as_view(), name='send_email'),
    #path('cheque-envoyer/', getChequeView.as_view(), name='cheque-envoyer'),
    path('cheque-envoyer/', chequeEnvoyer.as_view(), name='cheque-envoyer'),


    #path('demchq/', DemChqListAPIView.as_view(), name='demchq-list'),
    
    path('demchq/', MyDemChqListAPIView.as_view(), name='demchq-list'),
    path('agence/', AgenceListAPIView.as_view(), name='agence-list'),
    path('client/', ClientListAPIView.as_view(), name='client-list'),
    path('DemChqDt/', DemChqDtlListAPIView.as_view(), name='DemChqDt-list'),


    
]
