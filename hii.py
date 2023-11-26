import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSystemTrayIcon, QMenu, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime, Qt
from datetime import datetime, timedelta
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtMultimedia import QSoundEffect
from plyer import notification


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        uic.loadUi("ui/studyfocus.ui", self)
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.simple.clicked.connect(self.simplelevel)
        self.medium.clicked.connect(self.mediumlevel)
        self.intense.clicked.connect(self.intenselevel)
        self.custom.clicked.connect(self.customlevel)
        self.minimize.clicked.connect(self.minimize_to_system_tray)
        self.reset.clicked.connect(self.reset_timer)
        self.start.clicked.connect(self.start_timer)
        self.pause.clicked.connect(self.pause_resume_timer)
        self.paused = False
        self.elapsed_time = 0


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QIcon("resources/todo.png"))

        self.start_time = None
        self.elapsed_time = 0
        self.notification_shown = False
        self.notify_sound = "resources/notify.wav"  # Replace with the correct path to your sound file

        # Connect the button click to the appropriate level method
        self.simple.clicked.connect(self.simplelevel)
        self.medium.clicked.connect(self.mediumlevel)
        self.intense.clicked.connect(self.intenselevel)
        self.custom.clicked.connect(self.customlevel)
        self.start.clicked.connect(self.start_timer)
        self.reset.clicked.connect(self.reset_timer)
        self.minimize.clicked.connect(self.minimize_to_system_tray)
        self.pause.clicked.connect(self.pause_resume_timer)

        self.timer = QTimer(self)
        self.break_timer = QTimer(self)

        self.timer.timeout.connect(self.update_timer)
        self.break_timer.timeout.connect(self.break_timer_expired)

        self.create_system_tray_icon()

        self.break_duration_simple = timedelta(minutes=10)
        self.break_duration_medium = timedelta(minutes=20)
        self.break_duration_intense = timedelta(minutes=30)

        self.break_duration_custom = None  # Placeholder for custom break duration
        self.custom_settings_window = None

    def start_timer(self):
        if self.timer_label.text() == "00:00:00":
            # Display a QMessageBox indicating that a mode needs to be selected
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please select a mode before starting the timer.")
            msg.setWindowTitle("Mode Not Selected")
            msg.exec_()
        elif self.mode.text() in ["Simple", "Medium", "Intense", "Custom"]:
            self.start_time = datetime.now()
            self.elapsed_time = 0
            self.timer_duration = self.get_timer_duration()
            self.timer.start(1000)
            self.break_timer.start(1000)  # Start the break timer concurrently
            self.start.setEnabled(False)
            self.paused = False
            self.notification_shown = False

    def update_timer(self):
        if self.start_time and not self.paused:
            elapsed_time = self.elapsed_time + (datetime.now() - self.start_time).total_seconds()
            remaining_time = self.timer_duration.total_seconds() - elapsed_time

            if remaining_time <= 0:
                self.timer.stop()
                self.break_timer.stop()
                self.timer_label.setText("00:00:00")

                if not self.notification_shown:
                    self.show_notification("Break Time!", "Take a break and relax.")
                    self.notification_shown = True

                # Start the break timer with the appropriate duration
                self.break_timer_duration = self.get_break_duration()
                self.break_timer.start(50)

            else:
                hours,seconds = divmod(int(remaining_time), 3600)
                minutes, seconds = divmod(int(remaining_time), 60)
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time)

    def get_timer_duration(self):
        mode_text = self.mode.text()
        if mode_text == "Simple":
            return timedelta(seconds=10)
        elif mode_text == "Medium":
            return timedelta(hours=2)
        elif mode_text == "Intense":
            return timedelta(hours=3)
        elif mode_text == "Custom":
            return self.break_duration_custom if self.break_duration_custom else timedelta()

    def get_break_duration(self):
        mode_text = self.mode.text()
        if mode_text == "Simple":
            return self.break_duration_simple
        elif mode_text == "Medium":
            return self.break_duration_medium
        elif mode_text == "Intense":
            return self.break_duration_intense
        elif mode_text == "Custom":
            return self.break_duration_custom if self.break_duration_custom else timedelta()
    def break_timer_expired(self):
        break_duration = self.get_break_duration()

        if break_duration.total_seconds() <= 0:
            self.break_timer.stop()
            self.notification_shown = False
            self.show_notification("Back to Work!", "The next study session has started. Get back to work!")
            self.reset_timer()
            self.start_timer()
        else:
            hours, remainder = divmod(int(break_duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.setText(formatted_time)


    def simplelevel(self):
        self.timer_label.setText("00:00:10")
        self.mode.setText("Simple")

    def mediumlevel(self):
        self.timer_label.setText("02:00:00")
        self.mode.setText("Medium")

    def intenselevel(self):
        self.timer_label.setText("03:00:00")
        self.mode.setText("Intense")

    def customlevel(self):
        self.mode.setText("Custom")
        if not self.custom_settings_window:
            self.custom_settings_window = CustomSettingsWindow(self)
            self.custom_settings_window.show()

    def setup_animations(self):
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()

    def reset_timer(self):
        self.timer.stop()
        self.break_timer.stop()
        self.elapsed_time = 0
        text = self.mode.text()
        if text == "Simple":
            self.timer_label.setText("00:00:10")
        elif text == "Medium":
            self.timer_label.setText("02:00:00")
        elif text == "Intense":
            self.timer_label.setText("03:00:00")
        elif text == "Custom":
            self.timer_label.setText("00:00:00")
        self.start.setEnabled(True)  # Re-enable the start button
        self.paused = False

    def pause_resume_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.break_timer.stop()
            self.paused = True
            self.elapsed_time += (datetime.now() - self.start_time).total_seconds()
        else:
            if self.paused:
                self.start_time = datetime.now()
                self.timer.start(1000)
                self.break_timer.start(1000)
                self.paused = False
            else:
                self.start_time = datetime.now()
                self.timer.start(1000)
                self.break_timer.start(1000)
                self.paused = False
                self.start.setEnabled(False)

    def minimize_to_system_tray(self):
        self.hide()
        self.tray_icon.show_message("StudyFocus", "Application minimized to system tray.", QIcon("resources/todo.png"))

    def create_system_tray_icon(self):
        menu = QMenu(self)
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.show)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close_application)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("resources/logo.jpg"))
        self.tray_icon.setContextMenu(menu)

    def close_application(self):
        self.tray_icon.hide()
        sys.exit()

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon=None,  # e.g., "C:\\icon_32x32.ico"
            timeout=10,  # seconds
        )


class CustomSettingsWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("ui/custom_settings.ui", self)
        self.apply_button.clicked.connect(self.apply_settings)
        self.cancel_button.clicked.connect(self.close)

    def apply_settings(self):
        parent = self.parent()
        custom_duration_text = self.custom_duration.text()

        try:
            custom_duration = timedelta(minutes=int(custom_duration_text))
            parent.break_duration_custom = custom_duration
            parent.timer_label.setText(str(custom_duration))
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for custom duration.")

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
