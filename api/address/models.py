from django.db import models

from address.constants import DIST_DHAKA, DISTRICT_CHOICES


class Address(models.Model):
    building_and_street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    sub_district = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(
        max_length=255, choices=DISTRICT_CHOICES, default=DIST_DHAKA
    )
    country = models.CharField(max_length=255, default="Bangladesh")

    class Meta:
        ordering = ["-id"]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"{self.building_and_street}"
