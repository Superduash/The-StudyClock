import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import timedelta, datetime
from plyer import notification
from PyQt5.QtMultimedia import QSoundEffect

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List For Students")
        self.setGeometry(0,0,960,463)

        icon_path = "todolisticon.png"
        self.setWindowIcon(QIcon(icon_path))
        
        self.title = QLabel(self)
        self.title.setText("TO DO")
        self.title.setGeometry(0,0,960,0)

        layout = QVBoxLayout()
        container = QWidget(self)
        container.setLayout(layout)
        layout.addWidget(self.title)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-image: url(resources/bg.jpg); background-repeat: no-repeat; background-position: center; background-size: cover;")

        self.setCentralWidget(central_widget)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.show()
    sys.exit(app.exec_())




