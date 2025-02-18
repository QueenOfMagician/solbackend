from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import SigninSerializer, SignupSerializer

# Create your views here.


class SigninView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)

                return Response({
                    "status": "Login berhasil",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "id": user.id,
                    "username": user.username,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"status": "Password salah atau akun tidak ditemukan"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"status": "Validasi data gagal"}, status=status.HTTP_400_BAD_REQUEST)

def page404NotFound(request, exception):
    return render(request, '404.html', status=404)



class SignupView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "SUCCESS Created"}, status=status.HTTP_201_CREATED
            )
        return Response({"status": "Gagal Membuat Akun", "message": "Akun tidak dapat dibuat karena ada kesalahan pada input data."}, status=status.HTTP_400_BAD_REQUEST)

