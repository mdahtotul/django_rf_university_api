from django.contrib import admin

from .models import Payment, Enroll


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "trx_id",
        "amount",
        "store_amount",
        "status",
        "student",
    )


class EnrollAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "department",
        "payment",
        "price",
    )


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Enroll, EnrollAdmin)
