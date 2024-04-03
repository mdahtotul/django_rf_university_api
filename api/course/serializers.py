from rest_framework import serializers

from institute.serializers import RetrieveDepartmentSerializer

from .models import Course


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
