from rest_framework.permissions import BasePermission, SAFE_METHODS

from .constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER


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


class IsOwnerOrAdminOnly(BasePermission):

    def had_permission(self, request, view):
        if request.method == "POST":
            return True

        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        # Allow admins to edit/delete any parent object
        if request.user or request.user.role == ROLE_ADMIN:
            return True

        # Allow related user to edit/delete the parent object
        return obj.user == request.user
