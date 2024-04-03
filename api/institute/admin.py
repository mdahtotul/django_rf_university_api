from django.contrib import admin

from .models import Faculty, Department


class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "image")
    list_filter = ("name",)
    search_fields = ("name",)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "image")
    list_filter = ("name",)
    search_fields = ("name",)


admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
