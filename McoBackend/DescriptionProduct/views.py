import os
import requests
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

# ----------------------------
# Hugging Face API Setup
# ----------------------------
API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_TOKEN')}"}


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


def query(product_name: str):
    """Call Hugging Face API to generate description."""
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a product description generator. Output ONLY the description as instructed."
            },
            {
                "role": "user",
                "content": (
                    f"Write a professional, engaging, and SEO-friendly product description for '{product_name}'.\n\n"
                    "Format it exactly as follows:\n\n"
                    "### [Catchy Title]\n\n"
                    "[2–3 sentence opening paragraph]\n\n"
                    "* [Bullet point 1]\n"
                    "* [Bullet point 2]\n"
                    "* [Bullet point 3]\n"
                    "* [Bullet point 4]\n\n"
                    "[1 closing sentence encouraging purchase]\n\n"
                    "⚠️ IMPORTANT: Do not include reasoning, explanations, or extra text. Output ONLY the description."
                )
            }
        ],
        "model": "openai/gpt-oss-20b:together"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return {"error": response.text}
    try:
        return response.json()
    except Exception as ex:
        return {"error": f"Bad JSON: {ex}, Content: {response.text}"}


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

        # 🧠 Generate description
        output = query(product["product_name"])
        if (
            isinstance(output, dict)
            and "choices" in output
            and output["choices"]
            and "message" in output["choices"][0]
            and "content" in output["choices"][0]["message"]
        ):
            description = output["choices"][0]["message"]["content"].strip()
            # remove accidental reasoning if model leaks
            if "###" in description:
                description = description[description.index("###"):]
        elif "error" in output:
            description = f"Error from API: {output['error']}"
        else:
            description = "No text generated or wrong format."

        # 🏷️ Return full product data + AI description
        product_with_desc = dict(product)
        product_with_desc["description"] = description

        return Response(product_with_desc, status=status.HTTP_200_OK)
