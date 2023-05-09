import sys

from PyQt5.QtWidgets import QApplication


from controller import QuizController


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = QuizController()

    sys.exit(app.exec_())
