from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from django.conf import settings
import jwt

mongo_client = MongoClient(settings.MONGO_URI)
mongo_db = mongo_client.get_default_database()
USERS_COLLECTION = mongo_db['users']

class GetLoginDataAPIView(APIView):
    authentication_classes = []  # disable DRF's default JWT auth
    permission_classes = []      # disable DRF permission check

    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"error": "Authorization token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username = decoded.get("username")
            if not username:
                return Response({"error": "Invalid token claims"}, status=status.HTTP_401_UNAUTHORIZED)

            user_doc = USERS_COLLECTION.find_one({"username": username})
            if not user_doc:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            user_data = {
                "username": user_doc.get("username"),
                "user_id": user_doc.get("user_id"),
                "email": user_doc.get("email"),
                "first_name": user_doc.get("first_name"),
                "last_name": user_doc.get("last_name"),
                "phone_number": user_doc.get("phone_number"),
            }
            return Response(user_data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
