import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

app = QApplication([])
window = QMainWindow()
window.setWindowTitle("The StudyClock")
cw = QWidget()
window.setCentralWidget(cw)
layout = QVBoxLayout()
layout.addWidget(QLabel("Welcome to The StudyClock!!"))
layout.addWidget(QPushButton("Start Timer"))
layout.addWidget(QPushButton("Settings"))
cw.setLayout(layout)
window.show()

class StudyClockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Your main window initialization code will go here
        self.setWindowTitle("StudyClock")
        self.setGeometry(100, 100, 800, 600)
        self.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyClockApp()
    sys.exit(app.exec_())
