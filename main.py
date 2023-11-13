import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-image: url(resources/bg.jpg); background-repeat: no-repeat; background-position: center;")
        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()
        initial_width = screen_rect.width() * 1
        initial_height = screen_rect.height() * 0.966

        background_label = QLabel(self)
        background_label.setScaledContents(True)
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(background_label)

        self.setWindowTitle("The StudyClock")
        self.setGeometry(int((screen_rect.width() - initial_width) / 2), int((screen_rect.height() - initial_height) / 2), int(initial_width), int(initial_height))
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(self.size())
        icon_path = "resources/logo.jpg"
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon(icon_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
