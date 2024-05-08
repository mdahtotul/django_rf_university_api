from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import AdminOrReadOnly
from core.utils import format_exception
from core.exceptions import BadRequest
from .services import QuestionServices, QuestionUploadServices

questionServices = QuestionServices()
questionUploadServices = QuestionUploadServices()


class QuestionViewSet(APIView):
    permission_classes = [AdminOrReadOnly]

    def get(self, request):
        course_name = request.query_params.get("course_name")
        subject_name = request.query_params.get("subject_name")
        chapter_name = request.query_params.get("chapter_name")
        year = request.query_params.get("year")

        if subject_name is None or chapter_name is None:
            return BadRequest("Subject name and chapter name both parameters required")

        questions = questionServices.get_question(
            request=request,
            course=course_name,
            subject=subject_name,
            chapter=chapter_name,
            year=year,
        )

        return Response(questions, status=status.HTTP_200_OK)

    def post(self, request):
        course_name = request.data.get("course_name")
        subject_name = request.data.get("subject_name")
        chapter_name = request.data.get("chapter_name")
        year = request.data.get("year")
        stems = request.data.get("stems")

        total_questions = questionServices.add_question(
            course=course_name,
            subject=subject_name,
            chapter=chapter_name,
            year=year,
            stem_list=stems,
        )

        return Response(
            {"details": f"{total_questions} Question added successfully!"}, status=status.HTTP_201_CREATED
        )
        
    def handle_exception(self, exc):
        return format_exception(exc, self.request)
    

class QuestionDetailsViewSet(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, question_id):
        if question_id is None:
            raise BadRequest("Question Id parameter required")
        queryset = questionServices.get_question_by_id(question_id=question_id)
        return Response(queryset, status=status.HTTP_200_OK)
    
    def patch(self, request, question_id):
        if question_id is None:
            raise BadRequest("Question Id parameter required")
        question_text = request.data.get("question_text", None)
        option1 = request.data.get("option1", None)
        option2 = request.data.get("option2", None)
        option3 = request.data.get("option3", None)
        option4 = request.data.get("option4", None)
        option5 = request.data.get("option5", None)
        correct_ans = request.data.get("correct_ans", None)
        explanation = request.data.get("explanation", None)
        
        question_id = questionServices.edit_question(
            question_id=question_id, 
            question_text=question_text, 
            option1=option1, 
            option2=option2, 
            option3=option3, 
            option4=option4, 
            option5=option5, 
            correct_ans=correct_ans, 
            explanation=explanation
        )
        return Response({"details": f"question with id:{question_id} updated successfully"}, status=status.HTTP_200_OK)
    
    def delete(self, request, question_id):
        if question_id is None:
            raise BadRequest("Question Id parameter required")
        question_id = questionServices.delete_question(question_id=question_id)
        return Response({"details": f"question with id:{question_id} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def handle_exception(self, exc):
        return format_exception(exc, self.request)


class QuestionUploadViewSet(APIView):
    # permission_classes = [AdminOrReadOnly]

    def post(self, request):
        course_name = request.data.get("course_name")
        subject_name = request.data.get("subject_name")
        chapter_name = request.data.get("chapter_name")
        year = request.data.get("year")
        zip_file = request.FILES.get("zip_file")

        if course_name is None or subject_name is None or chapter_name is None:
            raise BadRequest("Course name and Subject name and chapter name parameters required")

        if zip_file is None:
            raise BadRequest("File not found")

        total_questions = questionUploadServices.upload_zipped_html_file(course=course_name,
            subject=subject_name, chapter=chapter_name, year=year, zip_file=zip_file
        )

        return Response(
            {"details": f"{total_questions} questions add successfully"},
            status=status.HTTP_201_CREATED,
        )

    def handle_exception(self, exc):
        return format_exception(exc, self.request)
