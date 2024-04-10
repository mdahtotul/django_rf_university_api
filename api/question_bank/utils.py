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
