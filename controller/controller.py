from view import MainWindow, QuizWidget, MainMenuWidget
from model import QuizModel
from constants import ThemeQuestion


class QuizController:

    def __create_quiz_wdg(self, theme_id: int):
        question: ThemeQuestion = self.model.get_question(theme_id, 1)
        if not question:
            # TODO: модальное окно с предупреждениемм
            return

        question_wdg = QuizWidget()
        question_wdg.BackToMenuBtn.clicked.connect(self.back_to_menu)
        question_wdg.ResetBtn.clicked.connect(self.reset_answer)
        question_wdg.CheckBtn.clicked.connect(self.check_answer)
        question_wdg.NextQuestionBtn.clicked.connect(self.next_question)
        question_wdg.PrevQuestionBtn.clicked.connect(self.prev_question)

        question_wdg.set_theme_name(self.model.get_theme_name(question.theme_id))
        question_wdg.set_question(question)

        self.model.set_current_question(question)

        return question_wdg

    def __create_main_menu_wdg(self):
        main_menu_wdg = MainMenuWidget()
        main_menu_wdg.ThemesComboBox.addItems([""] + list(self.model.themes.values()))
        main_menu_wdg.StartTestBtn.clicked.connect(self.start_quiz)

        return main_menu_wdg

    def __init__(self):

        # загрузим модель
        self.model = QuizModel()

        # загрузим представление
        self.view = MainWindow()
        self.view.setStyleSheet("font-size: 15px")
        self.view.setCentralWidget(self.__create_main_menu_wdg())
        self.view.show()

    def start_quiz(self):
        theme_id = self.view.centralWidget().ThemesComboBox.currentIndex()
        if theme_id != 0:
            self.view.setCentralWidget(self.__create_quiz_wdg(theme_id))

    def back_to_menu(self):
        # TODO: нужно ли сбрасывать результат при выходе в меню?
        self.model.reset_all_current_answers()
        self.view.setCentralWidget(self.__create_main_menu_wdg())

    def reset_answer(self):
        current_question = self.model.get_current_question()
        current_answers = [
            elem[0] for elem in self.model.get_current_answers()
        ]
        if current_question.correct_answer == set(current_answers):
            return

        self.view.centralWidget().reset_btns()
        for idx in current_answers:
            self.model.set_current_answer(idx, False)

    def check_answer(self):
        wdg = self.view.centralWidget()
        v_box_layout = wdg.VBox.layout()
        answer = set()
        for idx in range(v_box_layout.count()):
            btn = v_box_layout.itemAt(idx).widget()
            if btn.isChecked():
                answer.add(idx)

        current_question = self.model.get_current_question()
        self.model.reset_current_answers()
        for _id in answer:
            self.model.set_current_answer(_id, True)

        if answer == current_question.correct_answer:
            wdg.set_correct_question_label()
        else:
            wdg.set_incorrect_question_label()

    def next_question(self):
        wdg = self.view.centralWidget()
        next_question = self.model.get_next_question()
        if next_question:
            self.model.set_current_question(next_question)
            wdg.set_question(
                next_question,
                [elem[0] for elem in self.model.get_current_answers() if elem[1]]
            )

    def prev_question(self):
        wdg = self.view.centralWidget()
        prev_question = self.model.get_prev_question()
        if prev_question:
            self.model.set_current_question(prev_question)
            wdg.set_question(
                prev_question,
                [elem[0] for elem in self.model.get_current_answers() if elem[1]]
            )
