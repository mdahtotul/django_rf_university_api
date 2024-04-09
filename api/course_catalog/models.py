from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    total_questions = models.PositiveIntegerField(null=True, blank=True, default=0)

    class Meta:
        ordering = ["id"]
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self) -> str:
        return f"{self.id} -- {self.name}"


class Chapter(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    total_questions = models.PositiveIntegerField(null=True, blank=True, default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        ordering = ["id"]
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self) -> str:
        return f"{self.id} -- {self.name}"



