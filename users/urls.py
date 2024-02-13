from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Mytoken.as_view(), name='token_obtain_pair'),
    path('register/', RegisterAPI.as_view(), name='user-register'),
    path('password/', UpdatePassword.as_view(),name='update_password'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send_email/', SendEmailView.as_view(), name='send_email'),
    path('cheque-envoyer/', getChequeView.as_view(), name='cheque-envoyer'),
    
]
