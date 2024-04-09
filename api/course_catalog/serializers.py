from rest_framework import serializers

from course_catalog.models import Subject, Chapter, Year


class SimpleSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]


class SimpleChapterSerializer(serializers.ModelSerializer):
    subject = SimpleSubjectSerializer()

    class Meta:
        model = Subject
        fields = ["id", "name", "subject"]


class RetrieveSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "description",
            "total_questions",
        ]


class CreateUpdateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "name",
            "description",
            "total_questions",
        ]


class RetrieveChapterSerializer(serializers.ModelSerializer):
    subject = SimpleSubjectSerializer()

    class Meta:
        model = Chapter
        fields = [
            "id",
            "name",
            "description",
            "total_questions",
            "subject",
        ]


class CreateUpdateChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            "name",
            "description",
            "total_questions",
            "subject",
        ]


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = "__all__"
