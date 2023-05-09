
import os
from typing import Dict
from collections import defaultdict

from constants import AnswerTypes, ThemeQuestion


class QuizModel:
    ROOT_PROJECT_PATH = os.path.realpath(".")

    def __load_themes(self):
        themes_file = os.path.join(self.ROOT_PROJECT_PATH, "themes.txt")
        if os.path.exists(themes_file):
            with open(themes_file) as file:
                for line in file.readlines():
                    _id, name = line.strip().split(",")
                    self.themes[int(_id)] = name
        else:
            # TODO: добавить обработку
            raise Exception("Не найден файл с темами")

    def __load_questions(self):
        questions_files = [
            os.path.join(self.ROOT_PROJECT_PATH, f"questions_{i}.txt") for i in range(1, 2)  # len(self.themes) + 1)
        ]
        for question_file in questions_files:
            if os.path.exists(question_file):
                with open(question_file) as file:
                    while True:
                        line = file.readline()
                        if not line:
                            break

                        theme_id, question_id, answer_count = [int(elem) for elem in line.split(",")]
                        answer_type = file.readline().strip()
                        if answer_type not in (AnswerTypes.MULTI, AnswerTypes.ONLY_ONE):
                            raise Exception("Ошибка при разборе входного файла")
                        question = file.readline().strip()
                        answer_variants = tuple(((i, file.readline().strip()) for i in range(answer_count)))
                        answer = set(int(elem) for elem in file.readline().strip().split(","))

                        self.questions[theme_id][question_id] = ThemeQuestion(
                            theme_id,
                            question_id,
                            question,
                            answer_variants,
                            answer_type,
                            answer
                        )
            else:
                # TODO: добавить обработку
                raise Exception(f"Не найден файл {question_file} с вопросами")

    def __init__(self):
        self.themes: Dict[int, str] = {}
        self.questions: Dict[int, Dict[int, ThemeQuestion]] = defaultdict(dict)
        self.current_question = None
        self.current_answers: Dict[int, Dict[int, Dict[int, bool]]] = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(bool)
            )
        )

        self.__load_themes()
        self.__load_questions()

    def get_question(self, theme_id, question_id) -> ThemeQuestion:
        theme_questions = self.questions[theme_id]
        if question_id in theme_questions:
            return theme_questions[question_id]

    def get_next_question(self) -> ThemeQuestion:
        theme_questions = self.questions[self.current_question.theme_id]
        if self.current_question.id + 1 in theme_questions:
            return theme_questions[self.current_question.id + 1]

    def get_prev_question(self) -> ThemeQuestion:
        theme_questions = self.questions[self.current_question.theme_id]
        if self.current_question.id - 1 in theme_questions:
            return theme_questions[self.current_question.id - 1]

    def get_theme_name(self, theme_id) -> str:
        return self.themes.get(theme_id)

    def get_current_question(self) -> ThemeQuestion:
        return self.current_question

    def get_current_answers(self) -> list:
        return list(self.current_answers[self.current_question.theme_id][self.current_question.id].items())

    def set_current_question(self, question: ThemeQuestion) -> None:
        self.current_question = question

    def set_current_answer(self, answer_id: int, value: bool) -> None:
        self.current_answers[self.current_question.theme_id][self.current_question.id][answer_id] = value

    def reset_current_answers(self) -> None:
        self.current_answers[self.current_question.theme_id][self.current_question.id].clear()

    def reset_all_current_answers(self) -> None:
        self.current_answers.clear()
