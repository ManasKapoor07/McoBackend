import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductDescriptionSerializer  # use serializer for product_id validation


# ----------------------------
# MongoDB Setup
# ----------------------------
MONGO_URI = os.getenv("MONGO_URI")  # should include db name in URI
mongo_client = MongoClient(MONGO_URI)
MONGO_DB = mongo_client.get_default_database()  # auto picks db from URI
PRODUCTS_COLLECTION = MONGO_DB["Products"]


def get_product_by_id(product_id: str):
    """Return product dict for the given product_id (tries ObjectId, int, or str)."""
    product = None
    try:
        product = PRODUCTS_COLLECTION.find_one({"_id": ObjectId(product_id)})
    except Exception:
        try:
            product = PRODUCTS_COLLECTION.find_one({"id": int(product_id)})
        except Exception:
            product = PRODUCTS_COLLECTION.find_one({"id": str(product_id)})

    if product:
        product["_id"] = str(product["_id"])  # convert ObjectId for JSON serialization
    return product


class ProductDescriptionAPIView(APIView):
    def post(self, request):
        serializer = ProductDescriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data["product_id"]

        # 🔍 Find product in MongoDB
        product = get_product_by_id(product_id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Return product data without AI description
        return Response(product, status=status.HTTP_200_OK)
