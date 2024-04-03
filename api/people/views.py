from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import *
from core.utils import format_exception
from .models import Parent, Student, Teacher
from .filters import ParentFilter, StudentFilter, TeacherFilter
from .pagination import DefaultPagination
from .serializers import (
    CreateUpdateParentSerializer,
    CreateUpdateStudentSerializer,
    CreateUpdateTeacherSerializer,
    RetrieveParentSerializer,
    RetrieveStudentSerializer,
    RetrieveTeacherSerializer,
)


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    # queryset = Parent.objects.select_related("user", "address")
    serializer_class = RetrieveParentSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ParentFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateParentSerializer
        else:
            return RetrieveParentSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def handle_exception(self, exc):
        return format_exception(exc, self.request)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [StaffOrReadOnly | AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateStudentSerializer
        else:
            return RetrieveStudentSerializer

    def handle_exception(self, exc):
        return format_exception(exc, self.request)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = [AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateTeacherSerializer
        else:
            return RetrieveTeacherSerializer

    def handle_exception(self, exc):
        return format_exception(exc, self.request)
