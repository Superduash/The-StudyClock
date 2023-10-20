import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()
        initial_width = screen_rect.width() * 1
        initial_height = screen_rect.height() * 1

        self.setWindowTitle("The StudyClock")
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(initial_width, initial_height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())