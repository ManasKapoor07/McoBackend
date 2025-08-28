from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("McoBackend.products.urls")),
    path('api/signup/', include('McoBackend.signupMco.urls')),
    path('api/login/', include('McoBackend.signupMco.loginMco.urls'))

]
