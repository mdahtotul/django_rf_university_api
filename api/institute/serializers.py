from rest_framework import serializers

from .models import Department, Faculty


class RetrieveFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["id", "name", "description", "image", "created_at"]


class CreateUpdateFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["name", "description", "image"]


class RetrieveDepartmentSerializer(serializers.ModelSerializer):
    faculty = RetrieveFacultySerializer()

    class Meta:
        model = Department
        fields = ["id", "name", "description", "image", "created_at", "faculty"]


class CreateUpdateDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ["name", "description", "image", "faculty"]
