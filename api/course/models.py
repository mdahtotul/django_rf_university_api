import os
from uuid import uuid4
from django.db import models
from django.core.exceptions import ValidationError

from core.constants import SEMESTER_CHOICES, YEAR_CHOICES
from institute.models import Department


def course_thumbnail_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4().hex}{ext}"
    return os.path.join("course", filename)


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to=course_thumbnail_path, null=True, blank=True
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
    total_mcq_questions = models.PositiveIntegerField(null=True, blank=True, default=0)
    total_written_questions = models.PositiveIntegerField(
        null=True, blank=True, default=0
    )
    # adding one-to-many relationship between department and course. One department can have many courses
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    # Ensure that either year or semester contains data, but not both
    def clean(self):
        if self.year and self.semester:
            raise ValidationError(
                "Either year or semester can contain data, but not both."
            )
        elif not self.year and not self.semester:
            raise ValidationError("Either year or semester must contain data.")
