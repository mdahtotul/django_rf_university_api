from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response

from core.exceptions import BadRequest
from course_catalog.models import Chapter, Subject, Year
from .models import QuestionBank, QuestionMCQ, Stem


class QuestionServices:
    def get_question(self, subject: str, chapter: str, year):
        try:
            question_bank_query = Q(subject__name__iexact=subject) | Q(
                chapter__name__iexact=chapter
            )

            if year:
                question_bank_query &= Q(year__year__exact=year)

            question_bank = QuestionBank.objects.filter(question_bank_query).first()
            if not question_bank:
                return Response(
                    {"message": "No question bank found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            questions = QuestionMCQ.objects.filter(question_bank=question_bank.id)
            if not questions:
                return Response(
                    {"message": "No questions found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return questions
        except Exception as e:
            print(e)
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
                        options = question_obj.get("options", None)
                        explanation = question_obj.get("explanation", None)

                        options_text = [obj["option"] for obj in options]
                        options_text.extend([None] * (5 - len(options)))

                        correct_ans = [
                            idx
                            for idx, obj in enumerate(options, start=1)
                            if obj["is_correct"]
                        ]

                        mcq_question_list.append(
                            QuestionMCQ(
                                stem=stem if description else None,
                                question_text=question_text,
                                option1=options_text[0],
                                option2=options_text[1],
                                option3=options_text[2],
                                option4=options_text[3],
                                option5=options_text[4],
                                explanation=explanation,
                                correct_ans=correct_ans,
                                question_bank_id=question_bank_id,
                                tags=tags,
                            )
                        )

                    QuestionMCQ.objects.bulk_create(mcq_question_list)
        except Exception as e:
            raise e
