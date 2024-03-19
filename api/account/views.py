# External imports
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Internal imports
from core.permissions import *
from . import serializers
from .models import User
from .services.auth import AccountService
from .services.filters import UserFilterService
from .services.pagination import paginate_queryset

account_service = AccountService()
filter_service = UserFilterService()


class RegisterView(APIView):
    permission_classes = [AdminOnly]

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


class UsersView(APIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        name = request.query_params.get("name", None)
        email = request.query_params.get("email", None)
        phone = request.query_params.get("phone", None)
        page_size = request.query_params.get("page_size", 10)
        queryset = filter_service.user_filter_queryset(
            queryset=User.objects.all(),
            request=request,
            name=name,
            email=email,
            phone=phone,
        )

        return paginate_queryset(
            queryset,
            request,
            page_size=page_size,
            serializer_class=serializers.SimpleUserSerializer,
        )


class UserDetailsView(APIView):
    permission_classes = [AdminOnly]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = serializers.SimpleUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone = request.data.get("phone")
        avatar = request.FILES.get("avatar")

        data = account_service.update_old_user(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            avatar=avatar,
        )

        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
