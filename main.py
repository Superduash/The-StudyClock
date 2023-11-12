import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()
        initial_width = screen_rect.width() * 1
        initial_height = screen_rect.height() * 0.966
        self.setWindowTitle("The StudyClock")
        self.setGeometry((screen_rect.width() - initial_width) / 2, (screen_rect.height() - initial_height) / 2, initial_width, initial_height)
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(self.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
    icon_path = "path/to/your/icon.png"
    self.setWindowIcon(QIcon(icon_path))