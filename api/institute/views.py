from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from core.pagination import DefaultPagination
from core.permissions import AdminOrReadOnly
from core.utils import format_exception
from .filters import DepartmentFilter, FacultyFilter
from .models import Faculty, Department
from .serializers import (
    CreateUpdateDepartmentSerializer,
    CreateUpdateFacultySerializer,
    RetrieveDepartmentSerializer,
    RetrieveFacultySerializer,
)


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    permission_classes = [AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FacultyFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateFacultySerializer
        return RetrieveFacultySerializer

    def handle_exception(self, exc):
        return format_exception(exc, self.request)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepartmentFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateDepartmentSerializer
        return RetrieveDepartmentSerializer

    def handle_exception(self, exc):
        return format_exception(exc, self.request)
