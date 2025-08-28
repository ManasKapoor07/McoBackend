from rest_framework import serializers
from pymongo import MongoClient
from django.contrib.auth.hashers import check_password
import os

MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
MONGO_DB = mongo_client.get_default_database()
USERS_COLLECTION = MONGO_DB["users"]

class MongoLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user_doc = USERS_COLLECTION.find_one({"username": username})
        if not user_doc:
            raise serializers.ValidationError("Invalid username or password.")

        stored_password = user_doc.get("password")
        if not check_password(password, stored_password):
            raise serializers.ValidationError("Invalid username or password.")

        attrs['user'] = {
            "id": str(user_doc.get("_id")),
            "username": user_doc.get("username"),
            "email": user_doc.get("email"),
            "first_name": user_doc.get("first_name"),
            "last_name": user_doc.get("last_name"),
        }
        return attrs
