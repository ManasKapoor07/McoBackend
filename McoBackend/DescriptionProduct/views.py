import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductDescriptionSerializer

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_TOKEN')}"}

def query(product_name):
    payload = {
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Write a professional, engaging, and SEO-friendly product description for '{product_name}'. "
                    "Format it exactly as follows:\n\n"
                    "Do not include any internal reasoning, explanations, or extra text — only the final description in the above format.\n"
                    "### [Catchy Title]\n\n"
                    "[2–3 sentence opening paragraph]\n\n"
                    "* [Bullet point 1]\n"
                    "* [Bullet point 2]\n"
                    "* [Bullet point 3]\n"
                    "* [Bullet point 4]\n\n"
                    "[1 closing sentence encouraging purchase]\n"
                )
            }
        ],
        "model": "openai/gpt-oss-20b:together"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Hugging Face API status:", response.status_code)
    print("Raw response:", response.text)
    if response.status_code != 200:
        return {"error": response.text}
    try:
        return response.json()
    except Exception as ex:
        return {"error": f"Bad JSON: {ex}, Content: {response.text}"}

class ProductDescriptionAPIView(APIView):
    def post(self, request):
        serializer = ProductDescriptionSerializer(data=request.data)
        if serializer.is_valid():
            product_name = serializer.validated_data['product_name']
            output = query(product_name)
            # Properly parse chat/completions response
            if (
                isinstance(output, dict)
                and "choices" in output
                and output["choices"]
                and "message" in output["choices"][0]
                and "content" in output["choices"][0]["message"]
            ):
                generated = output["choices"][0]["message"]["content"]
            elif "error" in output:
                generated = f"Error from API: {output['error']}"
            else:
                generated = "No text generated or wrong format."
            return Response({
                "product_name": product_name,
                "description": generated
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
