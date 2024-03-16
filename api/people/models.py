from django.db import models
from django.conf import settings

from address.models import Address
from core.constants import (
    DEPARTMENT_CHOICES,
    DEPT_FISH,
    DESIGNATION_ASSOCIATE_PROFESSOR,
    DESIGNATION_ROLE_CHOICES,
    DESIGNATION_STUDENT,
    SEMESTER_CHOICES,
    YEAR_CHOICES,
)


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)


class Student(models.Model):
    session = models.CharField(max_length=10)
    semester = models.CharField(
        max_length=15,
        choices=SEMESTER_CHOICES,
        null=True,
        blank=True,
    )
    year = models.CharField(
        max_length=15,
        choices=YEAR_CHOICES,
        null=True,
        blank=True,
    )
    student_id = models.CharField(max_length=10, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    relationship_to_parent = models.CharField(max_length=255, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    enrollment_date = models.DateField(auto_now_add=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    credits = models.IntegerField(null=True, blank=True)
    designation = models.CharField(
        choices=DESIGNATION_ROLE_CHOICES,
        max_length=50,
        default=DESIGNATION_STUDENT,
    )
    department = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, default=DEPT_FISH
    )


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(
        choices=DESIGNATION_ROLE_CHOICES,
        max_length=50,
        default=DESIGNATION_ASSOCIATE_PROFESSOR,
    )
    department = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, default=DEPT_FISH
    )
    joined_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    specialist = models.TextField(null=True, blank=True)
