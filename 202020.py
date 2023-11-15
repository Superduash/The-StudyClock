import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPen, QCloseEvent
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QUrl
from datetime import datetime, timedelta
from plyer import notification
from PyQt5.QtMultimedia import QSoundEffect

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
        self.timer_label.setText("20:00")
        self.timer_label.setStyleSheet("font-family: 'Segoe UI'; color: #ffffff; font-size: 140px;")  # Enhanced font and color

        self.start_button = QPushButton("Start Timer", self)
        self.reset_button = QPushButton("Reset Timer", self)
        self.pause_button = QPushButton("Pause Timer", self)
        self.minimize_button = QPushButton("Minimize", self)

        button_width = 280
        button_height = 100
        font_size = 30
        font = QFont("Trebuchet MS", font_size, QFont.Bold)

        for button in [self.start_button, self.reset_button, self.pause_button, self.minimize_button]:
            button.setFixedSize(button_width, button_height)
            button.setFont(font)
            button.setStyleSheet(
                f"QPushButton {{ color: #ffffff; font-family: 'Segoe UI'; font-size: {font_size}px; background-color: #3498db; border: 2px solid #2980b9; padding: 5px; border-radius: 10px; }}"
                f"QPushButton:hover {{ background-color: #2980b9; }}"
            )

            # Add click effect animation
            self.add_click_effect_animation(button)

            # Add click sound effect
            button.clicked.connect(self.play_click_sound)

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)

        button_layout = QHBoxLayout()
        for button in [self.start_button, self.reset_button, self.pause_button, self.minimize_button]:
            button_layout.addWidget(button, alignment=Qt.AlignCenter)
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

        # Sound effect setup
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("path/to/click_sound.wav"))

    def add_click_effect_animation(self, button):
        effect = QPropertyAnimation(button, b"geometry")
        effect.setDuration(50)
        effect.setStartValue(button.geometry())
        effect.setEndValue(button.geometry().adjusted(5, 5, -5, -5))
        button.clicked.connect(effect.start)

    def play_click_sound(self):
        self.click_sound.play()

    def start_timer(self):
        if not self.timer.isActive():
            if hasattr(self, 'start_time') and self.start_time:
                elapsed_time = datetime.now() - self.start_time
                remaining_time = timedelta(minutes=1) - elapsed_time
                self.start_time = datetime.now() - (timedelta(minutes=1) - remaining_time)
            else:
                self.start_time = datetime.now()

            self.timer.timeout.emit()
            self.timer.start(1000)

    def reset_timer(self):
        self.timer.stop()
        self.timer_label.setText("20:00")

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

    def minimize_to_system_tray(self):
        self.hide()
        self.create_system_tray_icon()

    def update_timer(self):
        if self.start_time:
            elapsed_time = datetime.now() - self.start_time
            remaining_time = timedelta(minutes=1) - elapsed_time

            if remaining_time.total_seconds() <= 0:
                self.reset_timer()
                self.show_notification()
            else:
                formatted_time = str(remaining_time - timedelta(days=remaining_time.days)).split(".")[0]
                self.timer_label.setText(formatted_time)

    def create_system_tray_icon(self):
        menu = QMenu(self)
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.show)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close_application)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("resources/logo.jpg"))
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def close_application(self):
        self.tray_icon.hide()
        sys.exit()

    def closeEvent(self, event: QCloseEvent):
        if self.tray_icon is None:
            self.minimize_to_system_tray()
            event.ignore()
        else:
            self.create_system_tray_icon()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.show()
    sys.exit(app.exec_())