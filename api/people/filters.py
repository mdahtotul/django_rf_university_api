from django_filters import rest_framework as filters

from .models import Parent


class ParentFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name="user__first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="user__last_name", lookup_expr="icontains"
    )
    email = filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    phone = filters.CharFilter(field_name="user__phone", lookup_expr="icontains")

    class Meta:
        model = Parent
        fields = ["first_name", "last_name", "email", "phone", "occupation"]
