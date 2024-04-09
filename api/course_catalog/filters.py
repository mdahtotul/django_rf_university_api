from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet

from .models import Subject, Chapter


class SubjectFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Subject
        fields = ["name"]


class ChapterFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Chapter
        fields = ["name"]
