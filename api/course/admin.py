from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "department",
        "semester",
        "year",
    )


admin.site.register(Course, CourseAdmin)
