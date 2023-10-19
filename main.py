import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

app = QApplication(sys.argv)

class StudyClockApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Study Clock")
        self.initUI()

    def initUI(self):
        label = QLabel("Hello, Study Clock!", self)
        label.move(50, 50)

        button = QPushButton("Click Me", self)
        button.move(50, 100)
        button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        print("Button clicked!")

main_window = StudyClockApp()
main_window.show()

app.exec_()
