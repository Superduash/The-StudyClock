#importing required modules
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSoundEffect
from datetime import datetime, timedelta
from plyer import notification
from PyQt5 import uic, QtCore

# Load the UI file and set up the main window
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        uic.loadUi("ui/studyfocus.ui", self)
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.custom.clicked.connect(self.customlevel)

    def customlevel(self):
        self.click_sound.play()
        self.mode.setText("Custom")
        self.customwindow = QMainWindow()
        uic.loadUi("ui/studyfocuscustom.ui", self.customwindow)
        self.custom_timer_window()
        self.customwindow.show()

    def custom_timer_window(self):
        done_button = self.customwindow.findChild(QPushButton, 'save')
        self.length_of_session1 = self.customwindow.findChild(QTimeEdit, 'length_of_session')
        self.length_of_break1 = self.customwindow.findChild(QTimeEdit, 'length_of_break')
        done_button.clicked.connect(self.customaddons)

    # Function to handle custom timer window 'done' button click
    def customaddons(self):
        self.selected_time = self.length_of_session1.time()
        self.time_in_seconds = (-1) * self.selected_time.secsTo(QTime(0, 0))
        self.formatted_time = self.selected_time.toString("hh:mm:ss")
        self.timer_label.setText(self.formatted_time)
        self.selected_break_time = self.length_of_break1.time()
        self.break_time_in_seconds = (-1) * self.selected_break_time.secsTo(QTime(0, 0))
        self.formatted_break_time = self.selected_break_time.toString("hh:mm:ss")
        self.customwindow.close()

# Main window class that inherits from QMainWindow and the UI class
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Initialize the UI and set up fade in animations
        self.setupUi(self)
        self.setup_animations()
        self.setWindowIcon(QIcon("resources/todo.png"))

        # Initialize variables for timer, notification, and sound effects
        self.start_time = None
        self.elapsed_time = 0
        self.notification_shown = False
        self.notify_sound = "resources/notify.wav"

        # Connect signals to functions for various buttons
        self.simple.clicked.connect(self.simplelevel)
        self.medium.clicked.connect(self.mediumlevel)
        self.intense.clicked.connect(self.intenselevel)
        self.custom.clicked.connect(self.customlevel)
        self.start.clicked.connect(self.start_timer)
        self.reset.clicked.connect(self.reset_timer)
        self.minimize.clicked.connect(self.minimize_to_system_tray)
        self.pause.clicked.connect(self.pause_resume_timer)

        # Initialize sound effects and timers
        self.notify_sound = QSoundEffect()
        self.notify_sound.setSource(QUrl.fromLocalFile("resources/notify.wav"))
        self.notification_shown = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.break_timer = QTimer(self)
        self.break_timer.timeout.connect(self.update_break_timer)
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("resources/click1.wav"))

    # Function to start the timer
    def start_timer(self):
        if self.timer_label.text() == "00:00:00":
            # Display a warning if no mode is selected
            self.click_sound.play()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please select a mode before starting the timer.")
            msg.setWindowTitle("Mode Not Selected!!")
            msg.exec_()
        elif self.mode.text() in ["Simple", "Medium", "Intense", "Custom"]:
            # Start the timer based on the selected mode
            self.click_sound.play()
            self.start_time = datetime.now()
            self.elapsed_time = 0
            self.timer_duration = self.get_timer_duration()
            self.timer.start(20)
            self.start.setEnabled(False)
            self.paused = False
            self.notification_shown = False

    def update_timer(self):
        if self.start_time and not self.paused:
            elapsed_time = self.elapsed_time + (datetime.now() - self.start_time).total_seconds()
            remaining_time = self.timer_duration.total_seconds() - elapsed_time

            if remaining_time <= 0:
                # If the timer ends, switch to break and start break timer
                self.timer.stop()
                self.pause.clicked.disconnect(self.pause_resume_timer)
                self.pause.clicked.connect(self.break_pause_resume_timer)
                notification.notify(
                    title="Break Time!!",
                    message="It's break time! Take a break!",
                    timeout=5,
                )
                self.play_sound(self.notify_sound)
                mode_text = self.mode.text()
                if mode_text == "Simple":
                    self.timer_label.setText("00:15:00")
                elif mode_text == "Medium":
                    self.timer_label.setText("00:20:00")
                elif mode_text == "Intense":
                    self.timer_label.setText("00:30:00")
                elif mode_text == "Custom":
                    self.timer_label.setText(self.formatted_break_time)
                self.break_time = datetime.now()
                self.elapsed_time = 0
                self.break_time_duration = self.get_break_timer_duration()
                self.break_timer.start(50)
                self.start.setEnabled(False)
                self.paused = False
                self.notification_shown = False
            else:
                hours = int(remaining_time // 3600)
                minutes = int(remaining_time // 60 - (hours * 60))
                seconds = int(remaining_time - (hours * 3600) - (minutes * 60))
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time)

    def update_break_timer(self):
        if self.break_time and not self.paused:
            elapsed_time = self.elapsed_time + (datetime.now() - self.break_time).total_seconds()
            remaining_time = self.break_time_duration.total_seconds() - elapsed_time

            if remaining_time <= 0:
                # If the break timer ends, switch back to study timer
                self.break_timer.stop()
                self.pause.clicked.disconnect(self.break_pause_resume_timer)
                self.pause.clicked.connect(self.pause_resume_timer)
                notification.notify(
                    title="Break Ended",
                    message="Break is over! Time for another study session!",
                    timeout=5,
                )
                self.play_sound(self.notify_sound)
                mode_text = self.mode.text()
                if mode_text == "Simple":
                    self.timer_label.setText("01:00:00")
                elif mode_text == "Medium":
                    self.timer_label.setText("02:00:00")
                elif mode_text == "Intense":
                    self.timer_label.setText("03:00:00")
                elif mode_text == "Custom":
                    self.timer_label.setText(self.formatted_time)
                self.start_time = datetime.now()
                self.elapsed_time = 0
                self.timer_duration = self.get_timer_duration()
                self.timer.start(20)
                self.start.setEnabled(False)
                self.paused = False
                self.notification_shown = False
            else:
                hours = int(remaining_time // 3600)
                minutes = int(remaining_time // 60 - (hours * 60))
                seconds = int(remaining_time - (hours * 3600) - (minutes * 60))
                formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.timer_label.setText(formatted_time)

    # Function to get the duration of the study timer based on the selected mod
    def get_timer_duration(self):
        mode_text = self.mode.text()
        if mode_text == "Simple":
            return timedelta(hours=1)
        elif mode_text == "Medium":
            return timedelta(hours=2)
        elif mode_text == "Intense":
            return timedelta(hours=3)
        elif mode_text == "Custom":
            return timedelta(seconds=self.time_in_seconds)
        else:
            return timedelta()

    # Function to get the duration of the break timer based on the selected mode
    def get_break_timer_duration(self):
        mode_text = self.mode.text()
        if mode_text == "Simple":
            return timedelta(minutes=15)
        elif mode_text == "Medium":
            return timedelta(minutes=20)
        elif mode_text == "Intense":
            return timedelta(minutes=30)
        elif mode_text == "Custom":
            return timedelta(seconds=self.break_time_in_seconds)
        else:
            return timedelta()

    # Functions to set the timer label and mode for different difficulty levels
    def simplelevel(self):
        self.click_sound.play()
        self.timer_label.setText("01:00:00")
        self.mode.setText("Simple")

    def mediumlevel(self):
        self.click_sound.play()
        self.timer_label.setText("02:00:00")
        self.mode.setText("Medium")

    def intenselevel(self):
        self.click_sound.play()
        self.timer_label.setText("03:00:00")
        self.mode.setText("Intense")

    # Function to set up fade-in animation
    def setup_animations(self):
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.start()

    # Function to reset the timer to its initial state
    def reset_timer(self):
        self.click_sound.play()
        self.timer.stop()
        self.elapsed_time = 0
        text = self.mode.text()
        if text == "Simple":
            self.timer_label.setText("01:00:00")
        elif text == "Medium":
            self.timer_label.setText("02:00:00")
        elif text == "Intense":
            self.timer_label.setText("03:00:00")
        elif text == "Custom":
            self.timer_label.setText(self.formatted_time)
        self.start.setEnabled(True)
        self.paused = False

    def pause_resume_timer(self):
        if self.timer.isActive():
            # If the timer is active, pause it
            self.click_sound.play()
            self.timer.stop()
            self.paused = True
            self.elapsed_time += (datetime.now() - self.start_time).total_seconds()
        else:
            # If the timer is paused, resume it
            if self.paused:
                self.click_sound.play()
                self.start_time = datetime.now()
                self.timer.start(20)
                self.paused = False
            else:
                self.click_sound.play()
                self.start_time = datetime.now()
                self.timer.start(20)
                self.paused = False
                self.start.setEnabled(False)

    # Function to pause or resume the break timer
    def break_pause_resume_timer(self):
        if self.break_timer.isActive():
            # If the break timer is active, pause it
            self.click_sound.play()
            self.break_timer.stop()
            self.paused = True
            self.elapsed_time += (datetime.now() - self.break_time).total_seconds()
        else:
            # If the break timer is paused, resume it
            if self.paused:
                self.click_sound.play()
                self.break_time = datetime.now()
                self.break_timer.start(20)
                self.paused = False
            else:
                self.click_sound.play()
                self.break_time = datetime.now()
                self.break_timer.start(20)
                self.paused = False
                self.start.setEnabled(False)

    def minimize_to_system_tray(self):
        self.click_sound.play()
        self.hide()
        if not hasattr(self, 'tray_icon'):
            self.create_system_tray_icon()

    # Function to create the system tray icon and menu
    def create_system_tray_icon(self):
        menu = QMenu(self)
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.show)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close_application)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("resources/studying.png"))
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    # Function to close the application and hide the system tray icon
    def close_application(self):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        sys.exit()

    # Function to play a sound effect
    def play_sound(self, sound_effect):
        if sound_effect.isLoaded():
            sound_effect.play()
        else:
            print("Error: Sound file not loaded.")

# Entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
