from django.urls import path
from .views import signup
# from .LoginViews import LoginView  # Import login view from LoginViews.py in signupMco

urlpatterns = [
    path('', signup, name='signupMco'),          # Signup endpoint
    # path('', LoginView.as_view(), name='signupMco'),  # Login endpoint
]
