from rest_framework.permissions import BasePermission, SAFE_METHODS

from .constants import ROLE_ADMIN, ROLE_STAFF, ROLE_STUDENT, ROLE_USER


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.role == ROLE_ADMIN)


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == ROLE_ADMIN)


class StaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            return request.user.role == ROLE_STAFF
        else:
            return False


class StaffOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == ROLE_STAFF


class StudentOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            return request.user.role == ROLE_STUDENT
        else:
            return False


class StudentOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == ROLE_STUDENT


class UserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            return request.user.role == ROLE_USER
        else:
            return False


class UserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == ROLE_USER
