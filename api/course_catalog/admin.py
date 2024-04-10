from django.contrib import admin

from .models import Chapter, Subject, Year


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "total_questions")


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subject_name", "total_questions")

    def subject_name(self, obj):
        return obj.subject.name


class YearAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "total_questions")


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Year, YearAdmin)
