# External imports
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404

# Internal imports
from core import exceptions
from core.utils import is_valid_image
from account import serializers
from account.models import User


# User = settings.AUTH_USER_MODEL


class AccountService:
    def create_new_user(
        self,
        first_name: None,
        last_name: None,
        email: None,
        password: None,
        phone: None,
        avatar: None,
    ):
        try:
            if email is None or email == "":
                raise exceptions.BadRequest("Email is required!")
            elif password is None or password == "":
                raise exceptions.BadRequest("Password is required!")
            elif User.objects.filter(email=email).exists():
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

    def update_old_user(
        self,
        user,
        first_name: None,
        last_name: None,
        phone: None,
        avatar: None,
    ):
        try:
            if phone != "" and phone != None:
                if User.objects.filter(phone=phone).exists():
                    raise exceptions.ConflictError("Phone number already exists!")
                user.phone = phone

            if first_name != None and first_name != "":
                user.first_name = first_name
            if last_name != None and last_name != "":
                user.last_name = last_name

            if avatar is not None:

                if not is_valid_image(avatar):
                    raise exceptions.BadRequest("Invalid image!")

                user.avatar = avatar

            user.save()

            data = serializers.SimpleUserSerializer(user).data
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
