import glob
import os
from zipfile import ZipFile
from django.db import transaction
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from core.exceptions import BadRequest, NotFoundError
from core.settings import BASE_DIR
from course_catalog.models import Chapter, Subject, Year

from .serializers import RetrieveQuestionMCQSerializer
from .models import QuestionBank, QuestionMCQ, Stem
from .pagination import paginate_queryset
from .utils import FormatQuestionData, WebScrappingProcess, OSProcess

question_data_formatter = FormatQuestionData()
os_process = OSProcess()
scrapping = WebScrappingProcess()


class QuestionServices:
    def get_question(self, request, subject: str, chapter: str, year):
        try:
            question_bank_query = Q(subject__name__iexact=subject) & Q(
                chapter__name__iexact=chapter
            )

            if year:
                question_bank_query &= Q(year__year__exact=year)

            question_bank = QuestionBank.objects.filter(question_bank_query).first()
            if question_bank is None:
                raise NotFoundError("No question bank found")

            queryset = QuestionMCQ.objects.filter(question_bank=question_bank.id)

            if queryset is None:
                raise NotFoundError("No questions found")

            paginated_qs = paginate_queryset(
                queryset, request, 10, RetrieveQuestionMCQSerializer
            )
            paginated_data = paginated_qs.data

            serialized_data = question_data_formatter.format_question_data(
                paginated_data.get("results", [])
            )
            paginated_data["results"] = serialized_data
            return paginated_data

        except Exception as e:
            raise e

    def add_question(
        self,
        subject=str,
        chapter=str,
        year=None | str,
        stem_list=None | list,
    ):
        try:
            with transaction.atomic():
                # use old question bank if available otherwise create new one
                question_bank, created = QuestionBank.objects.get_or_create(
                    subject=Subject.objects.get(name__iexact=subject),
                    chapter=Chapter.objects.get(name__iexact=chapter),
                    year=Year.objects.get(year__exact=year),
                )
                question_bank_id = question_bank.id

                for stem_obj in stem_list:
                    description = stem_obj.get("description", None)
                    questions = stem_obj.get("questions", None)

                    # if stem description is not provided then create normal question
                    if description:
                        stem = Stem.objects.create(description=description)

                    # stem question will have more than one question
                    if description and len(questions) < 2:
                        raise BadRequest("Stem must have at least 2 questions")

                    mcq_question_list = []
                    for question_obj in questions:
                        question_text = question_obj.get("question_text", None)
                        tags = question_obj.get("tags", None)
                        option1 = question_obj.get("option1", None)
                        option2 = question_obj.get("option2", None)
                        option3 = question_obj.get("option3", None)
                        option4 = question_obj.get("option4", None)
                        option5 = question_obj.get("option5", None)
                        correct_ans = question_obj.get("correct_ans", None)
                        explanation = question_obj.get("explanation", None)

                        for ans in correct_ans:
                            if question_obj.get(f"option{ans}") is None:
                                raise BadRequest(
                                    f"Correct answer option{ans} has no data"
                                )

                        mcq_question_list.append(
                            QuestionMCQ(
                                stem=stem if description else None,
                                question_text=question_text,
                                option1=option1,
                                option2=option2,
                                option3=option3,
                                option4=option4,
                                option5=option5,
                                explanation=explanation,
                                correct_ans=correct_ans,
                                question_bank_id=question_bank_id,
                                tags=tags,
                            )
                        )

                    QuestionMCQ.objects.bulk_create(mcq_question_list)
        except Exception as e:
            raise e


class QuestionUploadServices:
    def upload_zipped_html_file(
        self, subject: str, chapter: str, year: None | str, zip_file
    ):
        root_folder = os.path.join(BASE_DIR, "media", "que_files")

        try:
            if os.path.exists(root_folder) is False:
                os.mkdir(root_folder)
            else:
                os_process.delete_contents_from_file_or_directory(root_folder)

            fs = FileSystemStorage(location=root_folder)
            fs.save(zip_file.name, zip_file)
            zip_file_path = glob.glob(os.path.join(root_folder, "*.zip"))[0]

            with ZipFile(zip_file_path, mode="r") as zf:
                zf.extractall(path=root_folder)

            htm_file_path = glob.glob(os.path.join(root_folder, "*.htm"))
            if not htm_file_path:
                raise BadRequest(".htm file not found")

            total_questions, content = scrapping.extract_question_list_from_htm(
                file_path=htm_file_path[0]
            )

            if len(content) > 0:
                formattedData = {
                    "subject": subject,
                    "chapter": chapter,
                    "year": year,
                    "stem_list": content,
                }

                QuestionServices().add_question(**formattedData)

                return total_questions
            else:
                raise BadRequest("No questions found")

        except Exception as e:
            raise e
