from django.urls import path
from .views import MongoLoginAPIView

urlpatterns = [
    path('', MongoLoginAPIView.as_view(), name='mongo-login'),
]
