from django.urls import path
from .views import ProductDescriptionAPIView

urlpatterns = [
    path('', ProductDescriptionAPIView.as_view(), name='generate-description'),
]
