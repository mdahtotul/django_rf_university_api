from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from core.utils import format_exception
from core.pagination import DefaultPagination
from core.permissions import AdminOrReadOnly

from .models import Course
from .filters import CourseFilter
from .serializers import CreateUpdateCourseSerializer, RetrieveCourseSerializer


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
