from django_filters import rest_framework as filters

from .models import Department, Faculty


class FacultyFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Faculty
        fields = ["name"]


class DepartmentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    faculty_name = filters.CharFilter(
        field_name="faculty__name", lookup_expr="icontains"
    )

    class Meta:
        model = Department
        fields = ["name", "faculty_name"]
