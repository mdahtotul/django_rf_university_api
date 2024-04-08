from rest_framework import serializers

from core.validations import SemesterYearSerializerValidations
from institute.serializers import RetrieveDepartmentSerializer

from .models import Course

yearSemesterValidation = SemesterYearSerializerValidations()


class RetrieveDepartmentCourseSerializer(serializers.ModelSerializer):
    department_id = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "code",
            "description",
            "thumbnail",
            "total_mcq_questions",
            "total_written_questions",
            "semester",
            "year",
            "department_id",
            "department_name",
        ]

    def get_department_id(self, obj):
        # Accessing the department ID through the Course object's department foreign key
        return obj.department.id

    def get_department_name(self, obj):
        # Accessing the department name through the Course object's department foreign key
        return obj.department.name


class RetrieveCourseSerializer(serializers.ModelSerializer):
    department = RetrieveDepartmentSerializer()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "code",
            "description",
            "thumbnail",
            "total_mcq_questions",
            "total_written_questions",
            "semester",
            "year",
            "department",
        ]


class CreateUpdateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            "name",
            "code",
            "description",
            "thumbnail",
            "total_mcq_questions",
            "total_written_questions",
            "semester",
            "year",
            "department",
        ]

    def validate(self, data):
        if self.instance:
            yearSemesterValidation.patch_method_validate(self.instance, data)
        else:
            yearSemesterValidation.post_method_validate(data)

        return data
