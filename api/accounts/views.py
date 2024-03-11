# External imports
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image

# Internal imports
from core.permissions import *
from .services.auth import AccountService

account_service = AccountService()


class UsersView(APIView):
    permission_classes = [AdminOrReadOnly]

    def post(self, request, format=None):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password")
        phone = request.data.get("phone")
        avatar = request.FILES.get("avatar")

        user = account_service.create_new_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            avatar=avatar,
        )

        return Response(user, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")

        user = account_service.login_user(email=email, password=password)

        return Response(user, status=status.HTTP_200_OK)
