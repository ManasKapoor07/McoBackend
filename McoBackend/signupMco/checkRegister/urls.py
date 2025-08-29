from django.urls import path
from .views import GetLoginDataAPIView

urlpatterns = [
    path('', GetLoginDataAPIView.as_view(), name='get-login-data'),
]
