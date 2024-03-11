# External imports
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from django.shortcuts import get_object_or_404
from PIL import Image

# Internal imports
from core import exceptions
from core.utils import is_valid_image
from accounts import serializers
from accounts.models import User


# User = settings.AUTH_USER_MODEL


class AccountService:
    def create_new_user(
        self,
        first_name: None,
        last_name: None,
        email: None,
        password: None,
        phone: str,
        avatar: None,
    ):
        try:
            if email is None or email == "":
                raise exceptions.BadRequest("Email is required!")
            if password is None or password == "":
                raise exceptions.BadRequest("Password is required!")
            if User.objects.filter(email=email).exists():
                raise exceptions.ConflictError("User already exists!")

            new_user = User.objects.create_user(
                email=email,
                password=password,
            )
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.phone = phone

            if avatar is not None:

                if not is_valid_image(avatar):
                    raise exceptions.BadRequest("Invalid image!")

                new_user.avatar = avatar

            new_user.save()

            data = serializers.SimpleUserSerializer(new_user).data
            return data
        except Exception as e:
            raise e

    def login_user(self, email: str, password: str):
        try:
            if email is None or email == "":
                raise exceptions.BadRequest("Email is required!")
            if password is None or password == "":
                raise exceptions.BadRequest("Password is required!")

            user = User.objects.filter(email=email).first()
            if not user:
                raise exceptions.UnAuthorizedError("Invalid credentials!")

            if not user.check_password(password):
                raise exceptions.UnAuthorizedError("Invalid credentials!")

            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

            if not user.is_first_login:
                user.is_first_login = True
                user.save(update_fields=["is_first_login"])

            data = serializers.LoginSerializer(user).data
            return data
        except Exception as e:
            raise e
