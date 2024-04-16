from docx.api import Document as ReadDocument


class FormatQuestionData:
    def single_question_format(self, data):
        return {
            "id": data.get("id"),
            "question_text": data.get("question_text"),
            "tags": data.get("tags"),
            "option1": data.get("option1"),
            "option2": data.get("option2"),
            "option3": data.get("option3"),
            "option4": data.get("option4"),
            "option5": data.get("option5"),
            "correct_ans": data.get("correct_ans"),
            "explanation": data.get("explanation"),
        }

    def format_question_data(self, data):
        """
        Formats a list of dictionaries containing question data into a structure
        with stems and nested questions.

        Args:
            data: A list of dictionaries representing questions.

        Returns:
            A list of dictionaries with stems and nested questions.
        """
        formatted_data = []
        current_stem = ""
        current_questions = []
        for item in data:
            if item.get("stem") != current_stem:
                # New stem, create a new entry with questions list
                current_stem = item.get("stem")
                current_questions = []
                formatted_data.append(
                    {"stem": current_stem, "questions": current_questions}
                )
            current_questions.append(self.single_question_format(item))

        return formatted_data


class FileUploadProcess:

    def extract_single_question(self, list_data: list, stem: str):
        question = {}

        question["stem"] = stem
        for item in list_data.split("[END]"):
            if item.strip().startswith("[QUESTION_BEGIN]") or item.strip().startswith(
                "[STEM_QUESTION_BEGIN]\n[QUESTION_BEGIN]"
            ):
                tag_str = item.strip().split("[TAGS]")[1]
                tags = tag_str.split(",")
                sanitized_tags = [tag.strip() for tag in tags]
                question["tags"] = sanitized_tags  # remove [TAGS] from the string
            elif item.strip().startswith("[QUESTION_TEXT]"):
                question["question_text"] = item.strip()[
                    len("[QUESTION_TEXT]") :
                ].strip()  # remove [QUESTION_TEXT] from the string
            elif item.strip().startswith("[OPTION_1]"):
                question["option_1"] = item.strip()[
                    len("[OPTION_1]") :
                ].strip()  # remove [OPTION_1] from the string
            elif item.strip().startswith("[OPTION_2]"):
                question["option_2"] = item.strip()[
                    len("[OPTION_2]") :
                ].strip()  # remove [OPTION_2] from the string
            elif item.strip().startswith("[OPTION_3]"):
                question["option_3"] = item.strip()[
                    len("[OPTION_3]") :
                ].strip()  # remove [OPTION_3] from the string
            elif item.strip().startswith("[OPTION_4]"):
                question["option_4"] = item.strip()[
                    len("[OPTION_4]") :
                ].strip()  # remove [OPTION_4] from the string
            elif item.strip().startswith("[OPTION_5]"):
                question["option_5"] = item.strip()[
                    len("[OPTION_5]") :
                ].strip()  # remove [OPTION_5] from the string
            elif item.strip().startswith("[CORRECT_ANSWER]"):
                ans = item.strip()[len("[CORRECT_ANSWER]") :].split(",")
                sanitized_ans = [int(item) for item in ans]
                question["CORRECT_ANSWER"] = sanitized_ans
            elif item.strip().startswith("[EXPLANATION]"):
                question["explanation"] = item.strip()[
                    len("[EXPLANATION]") :
                ].strip()  # remove [EXPLANATION] from the string

        return question

    def extract_data_from_docx(self, file_path):
        read_doc = ReadDocument(file_path)

        all_data = ""

        for p in read_doc.paragraphs:
            all_data += p.text
            all_data += "\n"

        all_questions = []

        for stem_question_data in all_data.split("[STEM_QUESTION_END]"):
            stem_lines = stem_question_data.strip().split("[END]")
            # print(stem_lines)
            stem_description = None
            extract_stem = stem_lines[0].strip().split("[STEM_DESCRIPTION]")
            if len(extract_stem) > 1:
                stem_description = extract_stem[1]

            for question_data in stem_question_data.split("[QUESTION_END]"):
                question = self.extract_single_question(question_data, stem_description)
                if bool(question) and len(question) > 1:
                    all_questions.append(question)

        print(all_questions)
        return all_questions


path = "d:/personal/django_rf_university_api/api/question_bank/QUESTION.docx"


FileUploadProcess().extract_data_from_docx(path)
