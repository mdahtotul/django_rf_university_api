from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Address

# Register your models here.
# admin@example.com - 1234


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "building_and_street",
        "postal_code",
        "district",
        "country",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "building_and_street",
                    "postal_code",
                    "sub_district",
                    "district",
                    "country",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "building_and_street",
                    "postal_code",
                    "sub_district",
                    "district",
                    "country",
                ),
            },
        ),
    )
    ordering = (
        "building_and_street",
        "-id",
    )


admin.site.register(Address, AddressAdmin)
