from django.contrib import admin

from .models import QuestionBank, QuestionMCQ, Stem


class QuestionBankAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
        "chapter",
        "year",
        "total_questions"
    )


admin.site.register(QuestionBank, QuestionBankAdmin)


class StemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
    )


admin.site.register(Stem, StemAdmin)


class QuestionMCQAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question_text",
        "stem",
        "explanation",
    )


admin.site.register(QuestionMCQ, QuestionMCQAdmin)
