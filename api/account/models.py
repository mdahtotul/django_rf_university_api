import os
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager

from core.constants import (
    GENDER_CHOICES,
    GENDER_MALE,
    ROLE_ADMIN,
    ROLE_USER,
    USER_ROLE_CHOICES,
)


def user_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4().hex}{ext}"
    return os.path.join("user", "avatar", filename)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError("Users must have an email address.")
        if password is None:
            raise TypeError("Users must have password.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None):
        if email is None:
            raise TypeError("Superusers must have an email address.")
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.role = ROLE_ADMIN

        user.save()
        return user


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, max_length=100, db_index=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default=GENDER_MALE
    )
    date_of_birth = models.DateField(null=True)
    password = models.CharField(max_length=100)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_image_path)
    phone = models.CharField(max_length=50, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default=ROLE_USER)
    is_verified = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.id} ---- {self.email}"


User = get_user_model()
