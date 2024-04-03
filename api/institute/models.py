import os

from uuid import uuid4
from django.db import models


def faculty_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4().hex}{ext}"
    return os.path.join("institute", "faculty", filename)


def department_image_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4().hex}{ext}"
    return os.path.join("institute", "department", filename)


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=faculty_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to=department_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self) -> str:
        return self.name
