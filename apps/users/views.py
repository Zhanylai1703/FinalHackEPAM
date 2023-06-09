from django.conf import settings
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import jwt 

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, DepartmentSerializer
from .models import User, Department



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny ,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        user_payload = {
            'user_id': user.id,
            'username': user.username
        }
        tokens = {
            'access_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256"),
            'refresh_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256")
        }
        response_data = {
            'user_id': user.id,
            'tokens': tokens

        }
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser]


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = [permissions.IsAdminUser]
