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

    # def validate(self, data):
    #     # Ensure that either year or semester contains data, but not both
    #     if data.get("year") and data.get("semester"):
    #         raise serializers.ValidationError(
    #             "Either year or semester can contain data, but not both."
    #         )
    #     elif not data.get("year") and not data.get("semester"):
    #         raise serializers.ValidationError(
    #             "Either year or semester must contain data."
    #         )

    #     return data

    # def create(self, validated_data):
    #     return Course.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.code = validated_data.get("code", instance.code)
    #     instance.description = validated_data.get("description", instance.description)
    #     instance.thumbnail = validated_data.get("thumbnail", instance.thumbnail)
    #     instance.total_mcq_questions = validated_data.get(
    #         "total_mcq_questions", instance.total_mcq_questions
    #     )
    #     instance.total_written_questions = validated_data.get(
    #         "total_written_questions", instance.total_written_questions
    #     )
    #     instance.semester = validated_data.get("semester", instance.semester)
    #     instance.year = validated_data.get("year", instance.year)
    #     instance.department = validated_data.get("department", instance.department)
    #     instance.save()
    #     return instance
