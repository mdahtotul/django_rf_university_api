from django_filters import rest_framework as filters

from .models import Subject, Chapter


class SubjectFilter(filters.FilterSet):
    class Meta:
        model = Subject
        fields = {
            "name": ["icontains"],
            "total_questions": ["exact"],
        }


class ChapterFilter(filters.FilterSet):
    class Meta:
        model = Chapter
        fields = {
            "name": ["icontains"],
            "total_questions": ["exact"],
        }
