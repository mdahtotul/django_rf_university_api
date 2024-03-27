from django_filters import rest_framework as filters

from .models import Parent, Student, Teacher


class ParentFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="user__first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="user__last_name", lookup_expr="icontains"
    )
    email = filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    phone = filters.CharFilter(field_name="user__phone", lookup_expr="icontains")
    occupation = filters.CharFilter(field_name="occupation", lookup_expr="icontains")

    class Meta:
        model = Parent
        fields = ["first_name", "last_name", "email", "phone", "occupation"]


class StudentFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="user__first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="user__last_name", lookup_expr="icontains"
    )
    email = filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    phone = filters.CharFilter(field_name="user__phone", lookup_expr="icontains")

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "phone"]


class TeacherFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="user__first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="user__last_name", lookup_expr="icontains"
    )
    email = filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    phone = filters.CharFilter(field_name="user__phone", lookup_expr="icontains")

    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "phone"]
