import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPen
from pystray import MenuItem as item, Icon as icon, Menu as menu
import pystray
from PyQt5.QtCore import Qt, QTimer, QSize
from datetime import datetime, timedelta
from plyer import notification
from PIL import Image

class OutlinedLabel(QLabel):
    def __init__(self, parent=None):
        super(OutlinedLabel, self).__init__(parent)
        self.text_color = QColor(255, 255, 255)
        self.outline_color = QColor(0, 0, 0)
        self.outline_size = 10

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        pen = QPen(QColor(self.outline_color))
        pen.setWidth(self.outline_size)
        painter.setPen(pen)

        for i in range(-self.outline_size, self.outline_size + 1):
            for j in range(-self.outline_size, self.outline_size + 1):
                if i**2 + j**2 <= self.outline_size**2:
                    painter.drawText(event.rect().adjusted(i, j, 0, 0), self.alignment(), self.text())

        painter.setPen(QColor(self.text_color))
        painter.drawText(event.rect(), self.alignment(), self.text())

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()
        initial_width = screen_rect.width() * 1
        initial_height = screen_rect.height() * 0.966

        self.setGeometry(int((screen_rect.width() - initial_width) / 2), int((screen_rect.height() - initial_height) / 2), int(initial_width), int(initial_height))
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(self.size())

        self.setWindowTitle("20-20-20 Rule Timer")

        icon_path = "resources/20-20-20.jpg"
        self.setWindowIcon(QIcon(icon_path))

        self.timer_label = OutlinedLabel(self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setText("00:00")
        self.timer_label.setStyleSheet("font-family: 'Trebuchet MS'; color: white; font-size: 140px;")  # Increased font size by 40%

        self.start_button = QPushButton("Start Timer", self)
        self.reset_button = QPushButton("Reset Timer", self)
        self.pause_button = QPushButton("Pause Timer", self)
        self.minimize_button = QPushButton("Minimize", self)
        self.menu = menu(
            item('Open', lambda icon, item: self.show()),
            item('Exit', lambda icon, item: self.close_application())
        )
        self.tray_icon = icon("name", self.create_icon(), menu=self.menu)
        button_size = QSize(300, 100)
        font_size = 24
        font = QFont("Trebuchet MS", int(font_size * 1.1), QFont.Bold)

        for button in [self.start_button, self.reset_button, self.pause_button, self.minimize_button]:
            button.setFixedSize(button_size)
            button.setFont(font)
            button.setStyleSheet(f"QPushButton {{ color: white; font-family: 'Trebuchet MS'; font-size: {int(font_size * 1.1)}px; background-color: transparent; border: 4px solid black; padding: 5px; }}")

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.minimize_button)
        layout.addLayout(button_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-image: url(resources/bg.jpg); background-repeat: no-repeat; background-position: center; background-size: cover;")

        self.setCentralWidget(central_widget)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.start_button.clicked.connect(self.start_timer)
        self.reset_button.clicked.connect(self.reset_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.minimize_button.clicked.connect(self.minimize_to_system_tray)

    def start_timer(self):
        if not self.timer.isActive():
            self.start_time = datetime.now()
            self.timer.start(1000)

    def reset_timer(self):
        self.timer.stop()
        self.timer_label.setText("00:00")

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()

    def show_notification(self):
        notification_title = "20-20-20 Rule Reminder"
        notification_message = "Look Away From The Screen For 20"
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon="resources/20-20-20.jpg",
            timeout=10
        )
    def update_timer(self):
        if self.start_time:
            elapsed_time = datetime.now() - self.start_time
            remaining_time = timedelta(minutes=20) - elapsed_time

            if remaining_time.total_seconds() <= 0:
                self.reset_timer()
                self.show_notification()
            else:
                formatted_time = str(remaining_time - timedelta(days=remaining_time.days)).split(".")[0]
                self.timer_label.setText(formatted_time)

    def create_system_tray_icon(self):
        self.menu = menu(
            item('Open', lambda icon, item: self.show()),
            item('Exit', lambda icon, item: self.close_application())
        )
        self.tray_icon = icon("name", self.create_icon(), menu=self.menu)
        self.tray_icon.run()

    def create_icon(self):
        return Image.open("resources/logo.jpg")

    def minimize_to_system_tray(self):
        self.hide()
        self.create_system_tray_icon()

    def close_application(self):
        self.tray_icon.stop()
        sys.exit()
    def closeEvent(self, event):
        if self.isVisible():
            self.minimize_to_system_tray()
            event.ignore()
        else:
            self.create_system_tray_icon()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.show()
    sys.exit(app.exec_())
