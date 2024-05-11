from django.db import models

from core.constants import ENROLL_CHOICES, ENROLL_F
from institute.models import Department
from people.models import Student


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    trx_id = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    store_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=100, choices=ENROLL_CHOICES, default=ENROLL_F)
    failed_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.student.user.email} | {self.trx_id} | {self.amount}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class Enroll(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.student.user.email} | {self.department.name}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Student Enroll"
        verbose_name_plural = "Student Enrolls"
