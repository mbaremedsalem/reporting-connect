from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Mytoken.as_view(), name='token_obtain_pair'),
    path('register/', RegisterAPI.as_view(), name='user-register'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
]