from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend

from core.utils import format_exception
from core.pagination import DefaultPagination
from core.permissions import AdminOrReadOnly

from .models import Course
from .filters import CourseFilter
from .serializers import (
    CreateUpdateCourseSerializer,
    RetrieveCourseSerializer,
    RetrieveDepartmentCourseSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateCourseSerializer
        return RetrieveCourseSerializer

    def handle_exception(self, exc):
        return format_exception(exc, self.request)


class DepartmentCourseViewSet(generics.ListAPIView):
    serializer_class = RetrieveDepartmentCourseSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_queryset(self):
        department_id = self.kwargs.get("department_id")
        queryset = Course.objects.filter(department_id=department_id)
        return queryset

    def handle_exception(self, exc):
        return format_exception(exc, self.request)
