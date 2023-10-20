import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The StudyClock")
        self.setWindowState(Qt.WindowMaximized)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())