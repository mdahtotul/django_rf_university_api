from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, RegexValidator

from address.models import Address
from institute.models import Department
from core.constants import (
    DEGREE_BSC,
    DEGREE_CHOICES,
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

    class Meta:
        ordering = ["-id"]
        verbose_name = "Parent"
        verbose_name_plural = "Parents"


class Student(models.Model):
    session = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(r"^\d{4}-\d{4}$", "Session format must be YYYY-YYYY.")
        ],
    )
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
    student_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r"^\d{1,8}$", "Only digits are allowed.")],
    )
    #  if the user record is deleted, the associated student record will also be deleted.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # if the associated parent record is deleted, this field will be set to null.
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True)
    relationship_to_parent = models.CharField(max_length=255, null=True, blank=True)
    # if the associated address record is deleted, this field will be set to null.
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    enrollment_date = models.DateField(auto_now_add=True)
    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MaxValueValidator(5.00)],
    )
    credits = models.IntegerField(null=True, blank=True)
    occupation = models.CharField(
        choices=DESIGNATION_ROLE_CHOICES,
        max_length=50,
        default=DESIGNATION_STUDENT,
    )
    # if the associated department record is attempted to be deleted, the deletion will be blocked due to the protect constraint.
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    degree = models.CharField(max_length=50, choices=DEGREE_CHOICES, default=DEGREE_BSC)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    occupation = models.CharField(
        choices=DESIGNATION_ROLE_CHOICES,
        max_length=50,
        default=DESIGNATION_ASSOCIATE_PROFESSOR,
    )
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    joined_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    qualifications = models.TextField(null=True, blank=True)
    specialist = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
