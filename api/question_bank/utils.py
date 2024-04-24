import re
import os
import base64
import shutil
from docx.api import Document as ReadDocument
from bs4 import BeautifulSoup

from core.settings import BASE_DIR
from core.exceptions import BadRequest


STEM_QUESTIONS_BEGIN = "[STEM_QUESTION_BEGIN]"
STEM_DESCRIPTION = "[STEM_DESCRIPTION]"
TOTAL_QUESTIONS = "[TOTAL_QUESTION]"
QUESTION_BEGIN = "[QUESTION_BEGIN]"
QUESTION_END = "[QUESTION_END]"
QUESTION_TEXT = "[QUESTION_TEXT]"
QUESTION_NUMBER = "[QUESTION_NUMBER]"
TAGS = "[TAGS]"
OPTION_1 = "[OPTION_1]"
OPTION_2 = "[OPTION_2]"
OPTION_3 = "[OPTION_3]"
OPTION_4 = "[OPTION_4]"
OPTION_5 = "[OPTION_5]"
CORRECT_ANSWERS = "[CORRECT_ANSWERS]"
EXPLANATION = "[EXPLANATION]"
STEM_QUESTION_END = "[STEM_QUESTION_END]"


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
            stem_description = None
            extract_stem = stem_lines[0].strip().split("[STEM_DESCRIPTION]")
            if len(extract_stem) > 1:
                stem_description = extract_stem[1]

            for question_data in stem_question_data.split("[QUESTION_END]"):
                question = self.extract_single_question(question_data, stem_description)
                if bool(question) and len(question) > 1:
                    all_questions.append(question)

        return all_questions


class WebScrappingProcess:
    def img_to_base64(self, img_tag):
        image_src = os.path.join(BASE_DIR, "media", "que_files", img_tag["src"])
        with open(image_src, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            img_tag["src"] = f"data:image/png;base64,{base64_image}"

    def sanitize_tags(self, content: str):
        clean_content = re.sub(r"<[^>]+>", "", content)
        return clean_content

    def remove_p_tag(self, paragraph: str, text_to_remove: str):
        # word htm file paragraph normally start with <p class="MsoNormal"
        match = '<p class="MsoNormal"'
        # extract text from index 0 to index len(match) and match that text with match string
        if match in paragraph[: len(match)]:
            # paragraph[paragraph.find(">") + 1 find the index of > that means full p tag
            # get actual data by extracting from index of > + 1 to len(paragraph) - len("</p>")
            paragraph = paragraph[
                paragraph.find(">") + 1 : len(paragraph) - len("</p>")
            ]
        # now remove the [QUESTION_NUMBER] text from paragraph
        if text_to_remove == QUESTION_NUMBER:
            paragraph = BeautifulSoup(paragraph, "html.parser").get_text()

        # return the paragraph without the text_to_remove
        return paragraph.replace(text_to_remove, "").strip()

    def parse_paragraph(
        self, paragraph, index: int, current_tag: str, stopping_tag: str
    ):
        # appears to remove specific HTML tags and text from the provided string
        temp = self.remove_p_tag(
            paragraph=str(paragraph[index]), text_to_remove=current_tag
        )

        for i in range(index + 1, len(paragraph)):
            if stopping_tag in paragraph[i].text.strip():
                break
            # if stopping tag is not found, add next paragraph line to temp variable
            temp += str(paragraph[i])
        # returns last index of the paragraph, and the parsed paragraph text
        return i, temp

    def extract_questions_from_stem(
        self,
        paragraph_tags,
        index: int,
    ):
        question_list = []
        for i in range(index, len(paragraph_tags)):
            if STEM_QUESTION_END in paragraph_tags[i].text.strip():
                break

            question_text = None
            tags = None
            option_1 = None
            option_2 = None
            option_3 = None
            option_4 = None
            option_5 = None
            correct_answer = None
            explanation = None

            text = paragraph_tags[i].text.strip()

            if text == QUESTION_BEGIN:
                # QUESTION_BEGIN line will not contain any text so go to next line which will contain the QUESTION_NUMBER
                idx = i + 1
                text = paragraph_tags[idx].text.strip()

                if QUESTION_NUMBER in text:
                    question_number = self.remove_p_tag(
                        paragraph=str(paragraph_tags[idx]),
                        text_to_remove=QUESTION_NUMBER,
                    )
                else:
                    raise BadRequest(
                        f"{QUESTION_NUMBER} not found in question {question_number}"
                    )

                # after getting que number go to the next line
                idx = idx + 1
                text = paragraph_tags[idx].text.strip()
                if TAGS in text:
                    idx, tags = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=TAGS,
                        stopping_tag=QUESTION_TEXT,
                    )
                    tag_list = [
                        tag.strip() for tag in self.sanitize_tags(tags).split(",")
                    ]

                else:
                    raise BadRequest(f"{TAGS} not found in question {question_number}")

                text = paragraph_tags[idx].text.strip()
                if QUESTION_TEXT in text:
                    idx, question_text = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=QUESTION_TEXT,
                        stopping_tag=OPTION_1,
                    )

                else:
                    raise BadRequest(
                        f"{QUESTION_TEXT} not found in question {question_number}"
                    )

                text = paragraph_tags[idx].text.strip()
                if OPTION_1 in text:
                    idx, option_1 = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=OPTION_1,
                        stopping_tag=OPTION_2,
                    )

                else:
                    raise BadRequest(
                        f"{OPTION_1} not found in question {question_number}"
                    )

                text = paragraph_tags[idx].text.strip()
                if OPTION_2 in text:
                    idx, option_2 = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=OPTION_2,
                        stopping_tag=OPTION_3,
                    )

                else:
                    raise BadRequest(
                        f"{OPTION_2} not found in question {question_number}"
                    )

                text = paragraph_tags[idx].text.strip()
                if OPTION_3 in text:
                    idx, option_3 = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=OPTION_3,
                        stopping_tag=OPTION_4,
                    )

                text = paragraph_tags[idx].text.strip()
                if OPTION_4 in text:
                    idx, option_4 = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=OPTION_4,
                        stopping_tag=OPTION_5,
                    )

                text = paragraph_tags[idx].text.strip()
                if OPTION_5 in text:
                    idx, option_5 = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=OPTION_5,
                        stopping_tag=CORRECT_ANSWERS,
                    )

                text = paragraph_tags[idx].text.strip()
                if CORRECT_ANSWERS in text:
                    idx, correct_answer = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=CORRECT_ANSWERS,
                        stopping_tag=EXPLANATION,
                    )
                    correct_answer_list = [
                        int(ans)
                        for ans in self.sanitize_tags(correct_answer).split(",")
                    ]

                else:
                    raise BadRequest(
                        f"{CORRECT_ANSWERS} not found in question {question_number}"
                    )

                text = paragraph_tags[idx].text.strip()
                if EXPLANATION in text:
                    idx, explanation = self.parse_paragraph(
                        paragraph=paragraph_tags,
                        index=idx,
                        current_tag=EXPLANATION,
                        stopping_tag=QUESTION_END,
                    )

                text = paragraph_tags[idx].text.strip()
                if QUESTION_END not in text:
                    raise BadRequest(
                        f"{QUESTION_END} not found in question {question_number}"
                    )

                formatted_question = {
                    "question_text": question_text,
                    "tags": tag_list,
                    "option1": option_1,
                    "option2": option_2,
                    "option3": option_3,
                    "option4": option_4,
                    "option5": option_5,
                    "correct_ans": correct_answer_list,
                    "explanation": explanation,
                }

                question_list.append(formatted_question)

        return question_list

    def extract_question_list_from_htm(self, file_path):
        with open(file_path, "r", encoding="utf8", errors="ignore") as f:
            stem_with_question_list = []
            total_questions = 0

            contents = f.read()
            soup = BeautifulSoup(contents, "html.parser")

            image_tags = soup.find_all("img")
            for img_tag in image_tags:
                self.img_to_base64(img_tag)

            paragraph_tags = soup.find_all("p")

            # storing stem description for multiple questions
            stem = None

            for i in range(len(paragraph_tags)):

                text = paragraph_tags[i].text.strip()

                if text == STEM_QUESTIONS_BEGIN:
                    idx = i + 1
                    text = paragraph_tags[idx].text.strip()

                    if STEM_DESCRIPTION in text:
                        idx, stem_description = self.parse_paragraph(
                            paragraph=paragraph_tags,
                            index=idx,
                            current_tag=STEM_DESCRIPTION,
                            stopping_tag=QUESTION_BEGIN,
                        )
                        stem = stem_description

                    question_list = self.extract_questions_from_stem(
                        paragraph_tags=paragraph_tags,
                        index=idx,
                    )

                    formatted_stem_with_questions = {
                        "description": stem if stem else None,
                        "questions": question_list,
                    }

                    stem_with_question_list.append(formatted_stem_with_questions)

            return total_questions, stem_with_question_list


class OSProcess:
    def delete_contents_from_file_or_directory(self, directory):
        # iterate over all files and folders in the given directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            # check if the item is a file
            if os.path.isfile(item_path):
                os.remove(item_path)  # delete the file

            # check if the item is a directory
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # delete the directory and its contents


# FileUploadProcess().extract_data_from_docx(path)
# htm_path = "d:/personal/django_rf_university_api/media/que_files/QUESTION_SCRAPPING.htm"
# WebScrappingProcess().extract_question_list_from_htm(htm_path)
