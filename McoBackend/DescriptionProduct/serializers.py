from rest_framework import serializers

class ProductDescriptionSerializer(serializers.Serializer):
    product_name = serializers.CharField(required=True, max_length=255)
