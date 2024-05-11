import glob
import os
from zipfile import ZipFile
from django.db import transaction
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from course.models import Course
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
    def get_question(self, request, course: str, subject: str, chapter: str, year):
        try:
            question_bank_query = (
                Q(course__name__iexact=course)
                & Q(subject__name__iexact=subject)
                & Q(chapter__name__iexact=chapter)
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
        course=str,
        subject=str,
        chapter=str,
        year=None | str,
        stem_list=None | list,
    ):
        try:
            with transaction.atomic():
                # use old question bank if available otherwise create new one
                course_obj = Course.objects.get(name__iexact=course)
                subject_obj = Subject.objects.get(name__iexact=subject)
                chapter_obj = Chapter.objects.get(name__iexact=chapter)
                year_obj = Year.objects.get(year__exact=year)

                question_bank, created = QuestionBank.objects.get_or_create(
                    course=course_obj,
                    subject=subject_obj,
                    chapter=chapter_obj,
                    year=year_obj,
                )
                question_bank_id = question_bank.id

                new_question_count = 0

                for stem_obj in stem_list:
                    description = stem_obj.get("description", None)
                    questions = stem_obj.get("questions", None)

                    # if stem description is not provided then create normal question
                    if description:
                        stem = Stem.objects.create(description=description)

                    # stem question will have more than one question
                    if description and len(questions) < 2:
                        raise BadRequest("Stem must have at least 2 questions")

                    new_question_count += len(questions)

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

                # updating total question count to related tables
                question_bank.total_questions += new_question_count
                question_bank.save()

                subject_obj.total_questions += new_question_count
                subject_obj.save()

                chapter_obj.total_questions += new_question_count
                chapter_obj.save()

                if year_obj:
                    year_obj.total_questions += new_question_count
                    year_obj.save()

                return new_question_count
        except Exception as e:
            raise e

    def get_question_by_id(self, question_id: int):
        try:
            question = QuestionMCQ.objects.filter(id=question_id).values().first()
            if question is None:
                raise NotFoundError("No question found")

            return question
        except Exception as e:
            raise e

    def edit_question(
        self,
        question_id: int,
        question_text: None | str,
        option1: None | str,
        option2: None | str,
        option3: None | str,
        option4: None | str,
        option5: None | str,
        correct_ans: None | list,
        explanation: None | str,
    ):
        try:
            question = QuestionMCQ.objects.filter(id=question_id).first()

            if question is None:
                raise NotFoundError("No question found")

            if question_text:
                question.question_text = question_text

            if option1:
                question.option1 = option1

            if option2:
                question.option2 = option2

            if option3:
                question.option3 = option3

            if option4:
                question.option4 = option4

            if option5:
                question.option5 = option5

            if correct_ans:
                new_ans = []
                for ans in correct_ans:
                    if ans and ans != "":
                        new_ans.append(int(ans))

                question.correct_ans = new_ans

            if explanation:
                question.explanation = explanation

            question.save()

            return question.id

        except Exception as e:
            raise e

    def delete_question(self, question_id):
        try:
            with transaction.atomic():
                question = QuestionMCQ.objects.get(id=question_id)
                if question is None:
                    raise NotFoundError("No question found")
                question_bank = QuestionBank.objects.get(id=question.question_bank_id)

                question.delete()
                # decrementing total questions count in related tables
                question_bank.total_questions -= 1
                question_bank.save()
                subject = Subject.objects.get(id=question_bank.subject_id)
                subject.total_questions -= 1
                subject.save()
                chapter = Chapter.objects.get(id=question_bank.chapter_id)
                chapter.total_questions -= 1
                chapter.save()
                if question_bank.year_id is not None:
                    year = Year.objects.get(id=question_bank.year_id)
                    year.total_questions -= 1
                    year.save()

                return question_id
        except Exception as e:
            raise e


class QuestionUploadServices:
    def upload_zipped_html_file(
        self, course: str, subject: str, chapter: str, year: None | str, zip_file
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
                    "course": course,
                    "subject": subject,
                    "chapter": chapter,
                    "year": year,
                    "stem_list": content,
                }

                new_question_count = QuestionServices().add_question(**formattedData)

                return new_question_count
            else:
                raise BadRequest("No questions found")

        except Exception as e:
            raise e
