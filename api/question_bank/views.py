from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.utils import format_exception
from .services import QuestionServices

questionServices = QuestionServices()


class QuestionViewSet(APIView):
    def get(self, request):
        subject_name = request.query_params.get("subject_name")
        chapter_name = request.query_params.get("chapter_name")
        year = request.query_params.get("year")

        if subject_name is None or chapter_name is None:
            return Response(
                {"message": "Subject name and chapter name both parameters required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions = questionServices.get_question(
            subject=subject_name,
            chapter=chapter_name,
            year=year,
        )

        return Response(questions, status=status.HTTP_200_OK)

    def post(self, request):
        subject_name = request.data.get("subject_name")
        chapter_name = request.data.get("chapter_name")
        year = request.data.get("year")
        stems = request.data.get("stems")
        # tags = request.data.get("tags")
        # total_questions = request.data.get("total_questions")

        # questions = request.data.get("questions")

        questionServices.add_question(
            subject=subject_name,
            chapter=chapter_name,
            year=year,
            stem_list=stems,
        )

        return Response(
            {"message": "Question added successfully!"}, status=status.HTTP_201_CREATED
        )

    def handle_exception(self, exc):
        return format_exception(exc, self.request)
