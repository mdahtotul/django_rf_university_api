from django.db import models
from django.contrib.postgres.fields import ArrayField

from course_catalog.models import Subject, Chapter, Year


class QuestionBank(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, default=None, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    marks_per_question = models.FloatField(default=1)
    has_negative_marking = models.BooleanField(default=False)
    negative_mark_value = models.FloatField(default=0.00)

    class Meta:
        verbose_name = "QuestionBank"
        verbose_name_plural = "QuestionBanks"

    def __str__(self) -> str:
        subject = self.subject.name
        chapter = self.chapter.name
        year = self.year.year

        return f"{self.id} - {subject} - {chapter} - {year} - {self.duration} min - {self.total_questions} questions"


class Stem(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Stem"
        verbose_name_plural = "Stems"

    def __str__(self) -> str:
        return f"{self.id} -- {self.description[:50]}"


class QuestionMCQ(models.Model):
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    stem = models.ForeignKey(Stem, on_delete=models.CASCADE, null=True, blank=True)
    tags = ArrayField(models.CharField(max_length=70), default=list)
    question_text = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField(blank=True, null=True)
    option4 = models.TextField(blank=True, null=True)
    option5 = models.TextField(blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    correct_ans = ArrayField(models.IntegerField(), default=list, size=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "MCQ Question"
        verbose_name_plural = "MCQ Questions"

    def __str__(self) -> str:
        return f"{self.id} -- {self.question_text[:50]}"
