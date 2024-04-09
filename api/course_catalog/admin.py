from django.contrib import admin

from .models import Chapter, Subject


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "total_questions")


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "total_questions")


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
