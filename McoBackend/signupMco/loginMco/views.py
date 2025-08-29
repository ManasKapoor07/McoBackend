from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from .serializers import MongoLoginSerializer

class MongoLoginAPIView(APIView):
    def post(self, request):
        serializer = MongoLoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user_info = serializer.validated_data['user']  # This is a dict
            print(user_info)
            # Manually create JWT tokens
            refresh = RefreshToken()
            # Set claims on refresh token
            refresh['user_id'] = user_info.get('id')
            refresh['email'] = user_info.get('email')
            refresh['username'] = user_info.get('username')

            # Get access token and set custom claims on it too
            access = refresh.access_token
            access['user_id'] = user_info.get('id')
            access['email'] = user_info.get('email')
            access['username'] = user_info.get('username')
            access.set_exp(lifetime=timedelta(minutes=15))

            return Response({
                "message": "Login successful",
                "user": user_info,
                "access": str(access),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
