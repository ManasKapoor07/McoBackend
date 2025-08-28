from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from .serializers import MongoLoginSerializer
class MongoLoginAPIView(APIView):
    def post(self, request):
        serializer = MongoLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_info = serializer.validated_data['user']  # This is a dict

            # Manually create tokens (no .id needed)
            refresh = RefreshToken()
            refresh['user_id'] = str(user_info.get('_id'))  # or 'id' depending on your dict
            refresh['email'] = user_info.get('email')

            access = refresh.access_token
            access.set_exp(lifetime=timedelta(minutes=15))  # optional: custom expiry

            return Response({
                "message": "Login successful",
                "user": user_info,
                "access": str(access),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
