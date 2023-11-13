import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
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

        title_label = QLabel(self)
        title_pixmap = QPixmap("resources/title.png")
        title_label.setPixmap(title_pixmap.scaledToWidth(initial_width * 0.3))
        title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Add a settings button
        settings_button = QPushButton("Settings", self)
        settings_button.clicked.connect(self.open_settings)
        settings_button.setStyleSheet("background-color: #3498db; color: white; border: 1px solid #297fb8; padding: 5px; border-radius: 5px;")
        settings_button.setMaximumWidth(100)  # Adjust the width as needed

        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(title_label)
        central_layout.addWidget(settings_button, alignment=Qt.AlignTop | Qt.AlignRight)

        self.setWindowTitle("The StudyClock")
        self.setGeometry(int((screen_rect.width() - initial_width) / 2), int((screen_rect.height() - initial_height) / 2), int(initial_width), int(initial_height))
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(self.size())

        icon_path = "resources/logo.jpg"
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon(icon_path))

    def open_settings(self):
        # Add your settings logic here
        print("Opening settings...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
