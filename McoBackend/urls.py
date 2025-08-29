from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("McoBackend.products.urls")),
    path('api/signup/', include('McoBackend.signupMco.urls')),
    path('api/login/', include('McoBackend.signupMco.loginMco.urls')),
    path('api/getLoginData/', include('McoBackend.signupMco.checkRegister.urls')),
    path('api/description-product/', include('McoBackend.DescriptionProduct.urls')),

]
