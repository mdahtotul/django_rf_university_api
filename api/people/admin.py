from django.contrib import admin

from .models import Parent, Student, Teacher


class ParentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "occupation",
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "student_id",
        "session",
        "department",
        "enrollment_date",
    )


class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "department",
        "joined_date",
    )


admin.site.register(Parent, ParentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
