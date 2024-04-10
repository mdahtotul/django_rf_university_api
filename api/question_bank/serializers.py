from rest_framework import serializers

from .models import QuestionMCQ


class RetrieveQuestionMCQSerializer(serializers.ModelSerializer):
    stem = serializers.SerializerMethodField()

    class Meta:
        model = QuestionMCQ
        fields = [
            "id",
            "stem",
            "question_text",
            "tags",
            "option1",
            "option2",
            "option3",
            "option4",
            "option5",
            "correct_ans",
            "explanation",
        ]

    def get_stem(self, instance):
        return instance.stem.description if instance.stem else None
