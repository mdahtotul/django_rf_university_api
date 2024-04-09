from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from core.utils import format_exception
from core.permissions import AdminOrReadOnly

from .models import Subject, Chapter
from .filters import SubjectFilter, ChapterFilter
from .serializers import (
    RetrieveSubjectSerializer,
    RetrieveChapterSerializer,
    CreateUpdateSubjectSerializer,
    CreateUpdateChapterSerializer,
)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = RetrieveSubjectSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateSubjectSerializer
        return RetrieveSubjectSerializer

    def handle_exception(self, exc):
        return format_exception(exc, self.request)


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = RetrieveChapterSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChapterFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateChapterSerializer
        return RetrieveChapterSerializer

    def handle_exception(self, exc):
        return format_exception(exc, self.request)
