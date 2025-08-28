from pathlib import Path
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# ----------------------------
# Base Setup
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]

# ----------------------------
# Installed Apps
# ----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    "corsheaders",
    "McoBackend.signupMco",
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    "rest_framework",     
    # Django REST Framework
    'McoBackend.products',
    'McoBackend.signupMco.loginMco',       # Your Products app
    # Your Products app
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
}
# ----------------------------
# Middleware
# ----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "https://m-co-qj1f.vercel.app",   # 👈 Replace with actual frontend URL
    "http://localhost:3000",                # for local React dev
]
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "https://m-co-qj1f.vercel.app/",
]
# ----------------------------
# URL & WSGI
# ----------------------------
ROOT_URLCONF = 'McoBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'McoBackend.wsgi.application'

# ----------------------------
# Django default DB (SQLite for admin/auth)
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------
# MongoDB Connection
# ----------------------------
MONGO_URI = os.getenv("MONGO_URI")  # fallback
mongo_client = MongoClient(MONGO_URI)
MONGO_DB = mongo_client.get_default_database()  # Picks DB from URI

# Example collection access
PRODUCTS_COLLECTION = MONGO_DB["Products"]

# ----------------------------
# Static files
# ----------------------------
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
