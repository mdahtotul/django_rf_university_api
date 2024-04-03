from django_filters import rest_framework as filters

from .models import Course


class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    semester = filters.CharFilter(field_name="semester", lookup_expr="icontains")
    year = filters.CharFilter(field_name="year", lookup_expr="icontains")
    department_name = filters.CharFilter(
        field_name="department__name", lookup_expr="icontains"
    )

    class Meta:
        model = Course
        fields = ["name", "code", "semester", "year", "department_name"]
