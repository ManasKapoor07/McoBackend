from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import re
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
MONGO_DB = mongo_client.get_default_database()
USERS_COLLECTION = MONGO_DB["users"]
COUNTERS_COLLECTION = MONGO_DB["counters"]

def get_next_user_id():
    """
    Get next sequence for user_id using MongoDB's counters collection.
    Ensures a unique, incrementing user_id starting from 1.
    """
    counter = COUNTERS_COLLECTION.find_one_and_update(
        {"_id": "user_id"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    # Mongo initializes the field to None, so if empty, start at 1.
    return counter["sequence_value"]

class SignUpSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)  # Read-only integer field for user ID
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    phone_number = serializers.CharField(required=False, max_length=15)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate_username(self, value):
        if USERS_COLLECTION.find_one({"username": value}):
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        email = value.lower().strip()
        if USERS_COLLECTION.find_one({"email": email}):
            raise serializers.ValidationError("Email is already registered.")
        return email

    def validate_phone_number(self, value):
        if value and not re.match(r"^\+?1?\d{9,15}$", value):
            raise serializers.ValidationError(
                "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user_id = get_next_user_id()
        user_data = {
            "user_id": user_id,  # Assign custom auto-incrementing ID
            "username": validated_data['username'],
            "email": validated_data['email'],
            "first_name": validated_data['first_name'],
            "last_name": validated_data['last_name'],
            "phone_number": validated_data.get('phone_number', ''),
            "password": make_password(validated_data['password']),
        }
        USERS_COLLECTION.insert_one(user_data)
        return user_data
