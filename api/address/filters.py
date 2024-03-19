from django_filters import rest_framework as filters

from .models import Address
from .constants import DISTRICT_CHOICES


class AddressFilter(filters.FilterSet):
    building_and_street = filters.CharFilter(lookup_expr="icontains")
    district = filters.ChoiceFilter(lookup_expr="icontains", choices=DISTRICT_CHOICES)
    country = filters.CharFilter(lookup_expr="icontains")
    postal_code = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Address
        fields = ["building_and_street", "district", "country", "postal_code"]
